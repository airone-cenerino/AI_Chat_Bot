import random
import os
import torch
import torch.nn as nn
import torch.optim as optim
import word_dict
import data_loader
import process_data
import network_model
import setting


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def maskNLLLoss(inp, target, mask):
    nTotal = mask.sum()
    crossEntropy = -torch.log(torch.gather(inp, 1, target.view(-1, 1)).squeeze(1))
    loss = crossEntropy.masked_select(mask).mean()
    loss = loss.to(device)
    return loss, nTotal.item()


# バッチを受け取って学習をする。
def train_batch(input_variable, lengths, target_variable, mask, max_target_len, encoder, decoder, embedding,
          encoder_optimizer, decoder_optimizer, batch_size, max_length=setting.MAX_SENTENCE_LENGTH):

    # 勾配初期化
    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()

    # GPU対応
    input_variable = input_variable.to(device)
    lengths = lengths.to(device)
    target_variable = target_variable.to(device)
    mask = mask.to(device)

    # Initialize variables
    loss = 0
    print_losses = []
    n_totals = 0

    encoder_outputs, encoder_hidden = encoder(input_variable, lengths)  # エンコーダー

    # Create initial decoder input (start with SOS tokens for each sentence)
    decoder_input = torch.LongTensor([[word_dict.SOS_token for _ in range(batch_size)]])
    decoder_input = decoder_input.to(device)

    # Set initial decoder hidden state to the encoder's final hidden state
    decoder_hidden = encoder_hidden[:decoder.n_layers]

    # Determine if we are using teacher forcing this iteration
    use_teacher_forcing = True if random.random() < setting.teacher_forcing_ratio else False

    # Forward batch of sequences through decoder one time step at a time
    if use_teacher_forcing:
        for t in range(max_target_len):
            decoder_output, decoder_hidden = decoder(
                decoder_input, decoder_hidden, encoder_outputs
            )
            # Teacher forcing: next input is current target
            decoder_input = target_variable[t].view(1, -1)
            # Calculate and accumulate loss
            mask_loss, nTotal = maskNLLLoss(decoder_output, target_variable[t], mask[t])
            loss += mask_loss
            print_losses.append(mask_loss.item() * nTotal)
            n_totals += nTotal
    else:
        for t in range(max_target_len):
            decoder_output, decoder_hidden = decoder(
                decoder_input, decoder_hidden, encoder_outputs
            )
            # No teacher forcing: next input is decoder's own current output
            _, topi = decoder_output.topk(1)
            decoder_input = torch.LongTensor([[topi[i][0] for i in range(batch_size)]])
            decoder_input = decoder_input.to(device)
            # Calculate and accumulate loss
            mask_loss, nTotal = maskNLLLoss(decoder_output, target_variable[t], mask[t])
            loss += mask_loss
            print_losses.append(mask_loss.item() * nTotal)
            n_totals += nTotal

    # Perform backpropatation
    loss.backward()

    # Clip gradients: gradients are modified in place
    _ = nn.utils.clip_grad_norm_(encoder.parameters(), setting.clip)
    _ = nn.utils.clip_grad_norm_(decoder.parameters(), setting.clip)

    # Adjust model weights
    encoder_optimizer.step()
    decoder_optimizer.step()

    return sum(print_losses) / n_totals


# バッチでのトレーニングを指定回数イテレーションする。
def trainIters(embedding, encoder, decoder, encoder_optimizer, decoder_optimizer, checkpoint, dict, pairs):
    print('モデルのトレーニングを開始します。')

    # iterationの回数だけバッチを作成する。
    #training_batches = [process_data.batch2TrainData(dict, [random.choice(pairs) for _ in range(setting.batch_size)]) for _ in range(setting.iteration_num)]

    # 初期化
    start_iteration = 1
    print_loss = 0
    if setting.IS_TRAIN_FROM_THE_MIDDLE:
        start_iteration = checkpoint['iteration'] + 1

    # イテレーションループ
    for iteration in range(start_iteration, setting.iteration_num + 1):
        #training_batch = training_batches[iteration - 1]
        training_batch = process_data.batch2TrainData(dict, [random.choice(pairs) for _ in range(setting.batch_size)])
        input_variable, lengths, target_variable, mask, max_target_len = training_batch        # トレーニング用データの展開

        # バッチを入力としてトレーニング
        loss = train_batch(input_variable, lengths, target_variable, mask, max_target_len, encoder,
                     decoder, embedding, encoder_optimizer, decoder_optimizer, setting.batch_size)
        print_loss += loss

        # 進捗状況の表示
        if iteration % setting.print_every == 0:
            print_loss_avg = print_loss / setting.print_every
            print("Iteration: {}; Percent complete: {:.1f}%; Average loss: {:.4f}".format(iteration, iteration / setting.iteration_num * 100, print_loss_avg))
            print_loss = 0

        # チェックポイントでセーブ。
        if (iteration % setting.save_every == 0):
            directory = os.path.join(setting.save_dir, setting.model_name, setting.corpus_name, '{}-{}_{}'.format(setting.encoder_n_layers, setting.decoder_n_layers, setting.hidden_size))

            if not os.path.exists(directory):
                os.makedirs(directory)

            torch.save({
                'iteration': iteration,
                'en': encoder.state_dict(),
                'de': decoder.state_dict(),
                'en_opt': encoder_optimizer.state_dict(),
                'de_opt': decoder_optimizer.state_dict(),
                'loss': loss,
                'embedding': embedding.state_dict()
            }, os.path.join(directory, '{}_{}.tar'.format(iteration, 'checkpoint')))


# モデルのトレーニングをする。
def execute_training_model(embedding, encoder, decoder, encoder_optimizer_sd, decoder_optimizer_sd, checkpoint, dict, pairs):
    # モデルをトレーニングモードにする。
    encoder.train()
    decoder.train()

    # optimizersのセットアップ
    encoder_optimizer = optim.Adam(encoder.parameters(), lr=setting.learning_rate)
    decoder_optimizer = optim.Adam(decoder.parameters(), lr=setting.learning_rate * setting.decoder_learning_ratio)
    if setting.IS_TRAIN_FROM_THE_MIDDLE:
        encoder_optimizer.load_state_dict(encoder_optimizer_sd)
        decoder_optimizer.load_state_dict(decoder_optimizer_sd)

    # If you have cuda, configure cuda to call
    for state in encoder_optimizer.state.values():
        for k, v in state.items():
            if isinstance(v, torch.Tensor):
                state[k] = v.cuda()

    for state in decoder_optimizer.state.values():
        for k, v in state.items():
            if isinstance(v, torch.Tensor):
                state[k] = v.cuda()


    # モデルのトレーニングをする。
    trainIters(embedding, encoder, decoder, encoder_optimizer, decoder_optimizer, checkpoint, dict, pairs)