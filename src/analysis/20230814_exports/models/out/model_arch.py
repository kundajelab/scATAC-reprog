"""
Written by Surag Nair. Should be comptable with tf1.14 and tf2.X.
"""

import keras

def bpnet_seq(seqlen=2000, filters=256, ndil=9):
    """
    Classic BPNet architecture with sequence-only input. Predicts profile
    logits and log-counts.

    Inputs and outputs both have length seqlen
    """

    inp = keras.Input((seqlen,4))

    x = keras.layers.Conv1D(filters, 
                            kernel_size=25, 
                            padding='same', 
                            activation='relu')(inp)

    for i in range(1, ndil+1):
        conv_x = keras.layers.Conv1D(filters, 
                                     kernel_size=3, 
                                     padding='same', 
                                     activation='relu', 
                                     dilation_rate=2**i)(x)
        x = keras.layers.add([conv_x, x])
    bottleneck = x     

    prof = keras.layers.Conv1D(1, 25, padding='same')(bottleneck)    
    prof = keras.layers.Flatten(name="logits")(prof)

    ct = keras.layers.GlobalAvgPool1D()(bottleneck)
    ct = keras.layers.Dense(1, name="logcounts")(ct)

    return keras.Model(inputs=inp, outputs=[prof,ct])


def chrombpnet(seqlen=2000, filters=256, ndil=9):
    """
    ChromBPNet architecture with sequence + bias counts + bias profile logits
    as inputs. Passes sequence through a bpnet_seq module. The counts output
    are logsumexp-ed with bias counts input, and the profile output is simply 
    added to the bias logits input.
    """

    # Inputs: sequence + (predicted) bias logits + (predicted) bias logcounts
    inp = keras.Input((seqlen,4))
    inp_bias_logits = keras.Input(shape=(seqlen,))
    inp_bias_logcounts = keras.Input(shape=(1,))

    # sequence is processed by bpnet_seq model
    seq_model = bpnet_seq(seqlen=seqlen,
                          filters=filters,
                          ndil=ndil)
    unbias_logits, unbias_logcounts = seq_model(inp)

    # PROFILE: predicted logits are simply a sum of unbias logits with 
    # (predicted) bias logits
    out_logits = keras.layers.Add(name="logits_w_bias")([unbias_logits, inp_bias_logits]) # <== add in bias logits
    
    # COUNTS: final count is log(exp(unbias_logcounts) + exp(inp_bias_logcounts)))
    concat_cts = keras.layers.concatenate([unbias_logcounts, inp_bias_logcounts],
                                          axis=-1)
    out_logcounts = keras.layers.Lambda(
                        lambda x: tf.math.reduce_logsumexp(x, axis=-1, keepdims=True),
                        name="logcounts_w_bias")(concat_cts)

    return keras.Model(inputs=[inp, inp_bias_logits, inp_bias_logcounts], 
                       outputs=[out_logits, out_logcounts])
