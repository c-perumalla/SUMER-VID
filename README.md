# SUMER-VID — Surgical Maneuver Recognition from Video

Recognizing the elementary maneuvers of open surgical technique — **hand ties**, **suture throws**, and **thread cuts** — from video of simulated procedures, as a step toward objective, automated assessment of surgical skill.

Research code from the [Pugh Lab](https://med.stanford.edu/pughlab.html), Department of Surgery, Stanford School of Medicine. Active development 2021; archived here for reference.

---

## Results

Three-class maneuver recognition on simulation video:

| Run | Encoder + head | Best val. accuracy | Notes |
|---|---|---|---|
| `model_2.1` | MobileNet (pretrained) + GRU | **0.927** | Best configuration |
| `model_2.2` | MobileNet (pretrained) + GRU | 0.922 | Reproduces 2.1 |
| `model_2.3` | MobileNet + GRU, tuned | 0.644 | |
| `model_1.2` | CNN (untrained) + GRU | 0.409 | Pre-transfer-learning baseline |
| `model_2.4`, `2.5`, `4.x`, `5.0` | various | ~0.339 | Chance for 3 classes — did not converge |

Surgical phase recognition on the public [Cholec80](http://camma.u-strasbg.fr/datasets) dataset:

| Run | Best val. accuracy |
|---|---|
| `model_3.2` | 0.927 |
| `model_3.3` | 0.890 |

Chance accuracy for the three-class task is 0.333. Several late runs (`2.4`, `2.5`, `4.0`, `4.1`, `5.0`) sit at exactly that, i.e. they collapsed to predicting a single class; they are kept here rather than deleted because the failures are part of the record.

### How to read these numbers

**The validation split is clip-level, not participant-level.** Training used `VideoFrameGenerator(split_val=0.33, shuffle=True)`, which partitions the set of 2-second clips at random. Because many clips derive from the same participant's session recording, near-duplicate clips appear on both sides of the split, and the reported accuracy is therefore **optimistic by an unquantified margin**.

A participant-wise holdout — all clips from a given surgeon confined to one side of the split — is the correct evaluation for this task and was not run. Any figure above should be read as an upper bound, not as an estimate of generalization to an unseen surgeon.

---

## Approach

**Data.** Video of surgical simulation sessions recorded at the American College of Surgeons 2019 meeting, with maneuver boundaries annotated in a spreadsheet. `slice_scripts/` join the annotation table to the session recordings and cut independent 2-second windows into per-class folders. `video_slicing_v2_background_class.py` additionally samples a *background* class from unannotated intervals, capped per participant to stop it from dominating.

**Models.** Two parallel implementations of the same idea — a CNN encoder applied per frame, with a recurrent head over the resulting sequence:

- *Keras* (`jupyter notebooks/`): `TimeDistributed` CNN → GRU, 5 frames at 100×100. The jump from an untrained encoder (`model_1.x`, ~0.41) to a pretrained MobileNet (`model_2.x`, ~0.92) is the single largest effect in these experiments.
- *PyTorch* (`pytorch_implementation/`): ResNet-50 → LSTM(2048→512) → FC, sequence length 3.

Notebooks are named `model_X.Y`, where `X` marks a structural change (GRU→LSTM, untrained→pretrained encoder) and `Y` a hyperparameter change. The convention is followed loosely.

**Cholec80 transfer.** `cholec80_experiments/` adapts published surgical-phase models to Cholec80: first a Keras reimplementation of [SV-RCNet](https://github.com/YuemingJin/SV-RCNet), then [MTRCNet-CL](https://github.com/YuemingJin/MTRCNet-CL). See that folder's README for attribution.

---

## Repository layout

```
slice_scripts/           annotation table + video -> labeled 2-second clips
jupyter notebooks/       Keras training and testing notebooks (model_X.Y)
pytorch_implementation/  ResNet-50 + LSTM, standalone PyTorch version
SUMERVID with SVR_CNET/  Keras reimplementation of SV-RCNet
cholec80_experiments/    Cholec80 transfer; adapted from MTRCNet-CL (see its README)
```

## Running this

```bash
pip install -r requirements.txt
```

Every script takes its input and output locations from constants at the top of the file, left empty and marked `# TODO: set local path`. Fill these in before running — start with `slice_scripts/video_slicing_v2.1.py` to build the clip dataset, then point a training notebook at the output folder.

## Limitations

- **The data is not public.** The simulation recordings and annotations are not redistributable, so nothing here runs end-to-end without access to them. Cholec80 is public and can be obtained from its maintainers.
- **No pinned environment.** `requirements.txt` lists the dependencies but not the versions these experiments were run against; the notebooks predate the current TensorFlow API in places.
- **Evaluation protocol**, as described above.
