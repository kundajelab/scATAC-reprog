## Loading model:

The models were trained using tf1.14. The models are provided in h5 format for tf1.14 (py3.7) and SavedModel format for tf2.X. 

tf2.X tested only for py3.8-10, tf2.8-11.

To load the models in tf1.14:
`python
model = tf.keras.models.load_model("path/to/model.h5")
`

In tf2:
`python
model = tf.keras.models.load_model("path/to/model_dir")
`

If all fails, you can load the architecture as provided in `model_arch.py` with default parameters (`bpnet_seq` for bias model and `chrombpnet` for chrombpnet model), and then load the weights using `model.load_weights` from the weights provided in the `weights` directory.

## Usage:
The bias models take as input one-hot sequence of length 2000. It has 2 outputs, a vector of logits of length 2000, and 1 logcounts scalar:

`python
# seq_one_hot of length B x 2000 x 4
out_bias_logits, out_bias_logcounts = bias_model.predict(seq_one_hot)

# out_bias_logits: B x 2000
# out_bias_logcounts: B x 1
`

The ChromBPNet model takes as input a one-hot sequence of length 2000, bias logits of length 2000 and bias log-counts scalar. It has the same output types as the bias model. To run the chrombpnet model to obtain predictions:
`python

pred_profile, pred_logcounts = chrombpnet_model.predict([seq_one_hot, out_bias_logits, out_bias_logcounts])

# pred_profile: B x 2000
# pred_logcounts: B x 1
`

If you wish to obtain the "de-biased" predictions (see methods), simply pass in zeros instead of the bias model predictions as:
`python
pred_profile_debiased, pred_logcounts_debiased = chrombpnet_model.predict([seq_one_hot, np.zeros((seq_one_hot.shape[0], 2000)), np.zeros((seq_one_hot.shape[0], 1))])
`

To obtain predicted per-base predicted counts (with or without bias):
`python
pred_per_base_counts = scipy.special.softmax(pred_profile, axis=-1) * (np.exp(pred_logcounts)-1)

# pred_per_base_counts: B x 2000
`

Note that in general predicted counts can't be compared across models as they are not corrected for sequencing depth.

## Note:

All bias models used across folds are identical, except for the final intercept term in the counts output (see Methods), that is specific to each cell state, fold combination.

## Folds:

| Fold | Test Chromosomes           | Validation Chromosomes        |
|------|----------------------------|-------------------------------|
| 0    | chr1                       | chr8, chr10                   |
| 1    | chr2, chr19                | chr1                          |
| 2    | chr3, chr20                | chr2, chr19                   |
| 3    | chr6, chr13, chr22         | chr3, chr20                   |
| 4    | chr5, chr16, chrY          | chr6, chr13, chr22            |
| 5    | chr4, chr15, chr21         | chr5, chr16, chrY             |
| 6    | chr7, chr18, chr14         | chr4, chr15, chr21            |
| 7    | chr11, chr17, chrX         | chr7, chr18, chr14            |
| 8    | chr9, chr12                | chr11, chr17, chrX            |
| 9    | chr8, chr10                | chr9, chr12                   |

Remaining chromosomes were used as the training chromosome for each fold.
