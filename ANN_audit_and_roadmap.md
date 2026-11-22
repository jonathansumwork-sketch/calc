# NEUR30006 final project: zip audit and roadmap

Scope: everything in `Artificial Neuro Final assignment.zip` (4,012 files, 46 MB), checked against the report (`ANN_2.docx`) and the student guide. No separate marking rubric was supplied, so "rubric alignment" below means alignment with the guide's objectives, constraints, report requirements and submission checklist.

Every number marked **(my rerun)** comes from scripts in `audit_scripts/`, which re-implement the network from `ANN_augmented.ipynb` (784-200-10, sigmoid, lr 0.1, 10 epochs, Rashid scaling). Run them from inside the unzipped project folder. They are an independent check, not your results, and you should reproduce them in your own notebook before putting any of them in the report.

---

## 1. Bottom line

- **The data is sound.** Dataset construction, the split and the 4x augmentation file all check out exactly.
- **The headline claim is not supported by what is in the zip.** The report says augmentation raised accuracy from 98.2% to 99.6%. Only the 99.6% (4x) run has saved code and output. The 98.2% baseline and the 99.4% threefold run have no code, no output and no data file in the zip.
- **A fair baseline appears to match the 4x model.** When the 500-image baseline is trained the same way as the 4x model (shuffled), it scores about 99.55%, indistinguishable from 4x. Trained on `symbols_training.csv` in file order (sorted by class, no shuffle), it scores about 86%. Neither is 98.2%.
- **The report's conclusion will probably have to change.** Plan on re-running the comparison and rewriting Results and Discussion around what the controlled run shows.

---

## 2. Does the data and code support the report?

| Report claim | Evidence in zip | Status |
|---|---|---|
| 10 classes, 1,000 images, 100 per class | `input_images_auto_review/` has 1,000 PNGs; every CSV row matches one exactly (500/500 exact matches) | Supported |
| 28x28, 8-bit grayscale, 0-255 | CSVs: 256 distinct values; 99.8% of non-zero pixels are intermediate grey, so images are genuinely anti-aliased | Supported |
| CSV = label + 784 values | 500x785, 500x785, 2000x785 | Supported |
| 500 train / 500 test, 50 per class, split before augmentation | Verified. Split is random with seed 42, stratified by class, no file in both sets | Supported |
| Test images independent of augmented data | No test image, or rotation of one, appears in the augmented file | Supported |
| 4x set = originals at 0, and rotations -10, +10, +20 | All 500 training images found at each of the four angles, labels correct. File is shuffled (seed 42) | Supported |
| 784-200-10, sigmoid, lr 0.1, 10 epochs | `ANN_augmented.ipynb` (executed) | Supported (for the 4x run only) |
| 4x accuracy 99.6% (498/500) and confusion matrix (4 as 2, 6 as 7) | Matches the executed notebook output | Supported, but see "no random seed" below |
| **Baseline 98.2% (491/500)** | **No baseline code or output anywhere in the zip.** I tried 24 baseline configurations (100 or 200 hidden nodes, 1/2/3/4/5/10 epochs, shuffled or not). With the report's settings: shuffled 497-498/500; file order 411-447/500 **(my rerun)**. 98.2% appeared in none | **Not supported / not reproducible** |
| **Threefold 99.4% (497/500)** | **No code, output or CSV for the threefold set.** Rebuilding it, I get 496-498/500 over 12 seeds (mean 99.32%) **(my rerun)**, so the figure is plausible but undocumented | **Undocumented** |
| "Same training settings across conditions" | Cannot be checked, because the baseline code is missing | Unknown |
| Symbols 0-4 angular, 5-9 curved | Judgement call. In Figure 1, symbol 8 has a straight-edged triangle and symbol 9 a straight-sided trapezoid with a small circle | Check wording |

### Why the baseline matters

Fair comparison runs, 12 seeds each, all on the same 500 test images **(my rerun)**:

| Condition | Correct /500 (range) | Mean accuracy |
|---|---|---|
| Baseline, `symbols_training.csv` in file order (class-sorted), 10 epochs | 411-447 | 85.9% |
| Baseline, shuffled every epoch, 10 epochs | 497-498 | 99.55% |
| Baseline, shuffled, 40 epochs (same number of weight updates as 4x) | 499 in all 12 | 99.80% |
| 3x (0, +10, +20), shuffled, 10 epochs | 496-498 | 99.32% |
| 4x file as submitted, 10 epochs | 497-498 | 99.50% |
| 4x, shuffled, 10 epochs | 497-499 | 99.58% |

Two things follow:

1. **Training order is a confound.** `symbols_training.csv` is sorted by class (all 0s, then 1s, and so on). The expander notebook shuffles the augmented file, so the augmented model sees mixed data while an unshuffled baseline sees class blocks. Training in class order is much worse.
2. **On the untouched test set there is no measurable augmentation effect.** The differences between shuffled baseline, 3x and 4x are at most one image out of 500, and a longer-trained baseline beats all of them.

I do not know how 98.2% was obtained. This is a hypothesis about the cause, not a finding.

Other reproducibility gaps:
- **No random seed.** `ANN_augmented.ipynb` sets none, so the exact two errors (4 as 2, 6 as 7) will not recur on a rerun.
- **Hard-coded paths.** `/Users/jj/Desktop/...` appears in `ANN_augmented.ipynb`, `expander_2026-1 (1).ipynb` and `conversion.ipynb`. Markers cannot run these as they are.

---

## 3. Contradictory material in the zip

`RANN_finish_project.ipynb` is the most recently modified notebook, and it describes a different experiment from the report:

| | Report / `ANN_augmented.ipynb` | `RANN_finish_project.ipynb` |
|---|---|---|
| Hidden nodes | 200 | 100 |
| Epochs | 10 | 4 |
| Augmentation | -10, 0, +10, +20 rotations | -8, +8 rotations and a 1-pixel shift |
| Run state | executed | **no outputs saved** |

It also describes the images as having "different sizes/stroke thicknesses", which is not what the preprocessing does (see section 4). It also seeds the network (123) and uses `hnodes` for the first-layer weight scaling where the course code uses `inodes`. Either remove it from the submission or rewrite it so it is the single, executed notebook that matches the report.

---

## 4. Findings that bear on the report's argument

1. **Preprocessing removes scale and position variation.** Each drawing was cropped to its ink, shrunk to fit within 22x22 (aspect ratio kept), centred on a 28x28 canvas, then inverted to white-on-black. Every class has a maximum dimension of about 20-21 px. This is a defensible reason for using rotation only, because translation and scaling add little here, and it belongs in Methods.
2. **The classes are very well separated.** The nearest training image to a test image is of the same class for 499 of 500 test images (median distance 573 same-class vs 968 other-class). A ceiling near 99.5% is expected, which limits what the clean test set can show **(my rerun)**.
3. **No duplicate images; no blank or tiny images.** The lowest-ink images are mostly class 1 (about 23-30 ink pixels), which is plausible for a thin stroke.
4. **Where augmentation does help is robustness.** I rotated copies of the test images for analysis only (never in training) and compared a shuffled baseline with the 4x model, 4 seeds each **(my rerun)**:

   | Test rotation | -30 | -20 | -10 | 0 | +10 | +20 | +30 |
   |---|---|---|---|---|---|---|---|
   | Baseline | 47% | 82% | 98% | 99.5% | 99% | 84% | 58% |
   | 4x augmented | 57% | 95% | 99% | 99.5% | 99.5% | 99% | 91% |

   The benefit is lopsided: training covered -10 to +20, and the model is much stronger at +20 and +30 than at -20 and -30.
5. **The confusable pairs under rotation match the report's two errors.** For the baseline at -20 and +20, the top confusions (counts pooled over 3 seeds) were, at -20: 6 as 1 (101), 2 as 4 (51), 4 as 1 (44); at +20: 4 as 2 (78), 1 as 6 (46), 7 as 6 (31) **(my rerun)**. The report's 4 as 2 and 6 as 7 errors involve the same classes. This offers a design-based explanation the current Discussion lacks, once you have reproduced it in your own notebook.

---

## 5. Alignment with the guide

| Guide requirement | Status | Note |
|---|---|---|
| Design 10 original symbols with classification in mind | Met | Original; angular/curved structure and a deliberate 3/7 lookalike pair |
| Dataset of about 1,000-4,000 labelled images | Met | 1,000 |
| 256-level anti-aliased grayscale, 28x28 | Met | Verified; Methods does not describe the conversion |
| Half held out before augmentation | Met | Verified |
| Baseline with accuracy, training count, classes, hyperparameters, epochs | **Gap** | No baseline code or output; numbers cannot be reproduced |
| Augmentation applied and justified | Partial | Applied correctly; the choice of angles is not justified, and the 3x condition has no code |
| Augmented set about 4x larger | Met | 2,000 |
| Measure change in performance | **Gap** | Confounded by training order; single run per condition |
| Final submission: train/test data, ANN code, augmentation code, report | Partial | See section 6 |
| Report 1,500 words | Met | Revised draft is about 1,400 words including captions |
| Introduction states design principles, assumptions and expected confusions | Partial | Improved in the revision; assumptions remain thin |
| Methods covers changes to the standard code and any extra tests | Gap | No preprocessing, split, shuffling, seeds or augmentation implementation |
| Results show symbols plus baseline and augmented performance | Partial | Symbols and 4x shown; baseline/3x not reproducible |
| Discussion explains the design/augmentation/ANN interaction | **Weakest part** | Mostly "cannot tell"; the rotation-fragile pairs are the missing insight |
| Visual abstract | Met in the revised file | Must be updated if numbers change |

---

## 6. Submission package

The guide's checklist needs the training set, test set, ANN code, augmentation code and report. The current zip has 4,012 files that include:

- Three superseded image folders (`input_images_full` is incomplete, 674 files, from a crashed run; `input_images_corrected`; `input_images_final`). Only `input_images_auto_review` corresponds to the CSVs.
- `.ipynb_checkpoints/`, `.DS_Store`, `qc_backups/`, `class_0_practice.csv`, `class_0_antialiased_practice.csv`, `bigger_set.csv` (identical content to `symbols_training_augmented.csv`) and the whole `makeyourownneuralnetwork-master` course repo.
- 40 source PDFs and an unexecuted, contradictory `RANN_finish_project.ipynb`.

Keep: the three CSVs, one executed experiment notebook, one augmentation notebook (with relative paths), the report, and optionally `input_images_auto_review/` and the source PDFs as provenance. Remove the rest.

The brief gives the submission address as `pkitc@unimelb.edu`, which looks truncated; confirm it before sending. Subject line must be exactly `final_project NEUR30006`.

---

## 7. Roadmap to completion

### Phase 1: fix the experiment (about 2-3 hours)
1. Create one clean notebook, `final_experiment.ipynb`, with relative paths.
2. Write one training function: fixed hidden nodes, learning rate and epochs, **shuffled every epoch**, and a seed argument.
3. Generate the 3x set (0, +10, +20) in code, from the same rotation function used for 4x. State the rotation direction (positive = anticlockwise in scipy's `rotate`, which I confirmed).
4. Train baseline, 3x and 4x on the same settings, **10 seeds each**. Report mean and standard deviation, and save the executed outputs.
5. Optional control: baseline trained for 40 epochs, which gives it the same number of weight updates as 4x at 10 epochs. This addresses the objection that augmentation only adds training.
6. Save the confusion matrix and per-class accuracy for each condition.

### Phase 2: decide the story from the evidence (about 1 hour)
1. If the controlled comparison shows no clean-test gain (expected), say so plainly. A null result with a ceiling explanation is a legitimate finding and is better than an unreproducible gain.
2. Add the robustness analysis: evaluate the same trained models on rotated test copies (analysis only; the headline test stays untouched). Include it as a clearly labelled secondary test.
3. Decide how you justify the asymmetric angles (-10 to +20). Either give a reason, or run a symmetric condition (-20 to +20) and report it.
4. Look at the actual misclassified images for the confusable pairs (4/2 and 6/1/7), because that is the design-level insight the brief asks for.

### Phase 3: rewrite the report (about 3 hours, within 1,500 words)
Suggested budget:

| Section | Words | Must contain |
|---|---|---|
| Introduction | about 250 | Design principles, why rotation, the hypothesis, expected confusions |
| Methods | about 300 | Goodnotes drawing; PDF rendering; crop, Lanczos resize, centring and inversion (this removes scale/position variation, so rotation is the relevant augmentation); stratified random split (seed 42); ANN settings; shuffling; seeds and number of runs; rotation implementation |
| Results | about 300 | Table with mean +/- SD for each condition; one confusion matrix; the robustness figure |
| Discussion | about 550 | Effect of augmentation vs ceiling; which pairs are rotation-fragile and why; the angle-range asymmetry; design lessons; limitations (one drawer, sequential same-session drawings, small test set, one augmentation type) |
| Remaining | about 100 | Captions and conclusion |

Then re-build the visual abstract with the final numbers. Keep the earlier rule: every claim must come from your own saved output.

### Phase 4: package and submit (about 1 hour)
1. Build a clean folder per section 6; run the notebooks top to bottom on a fresh kernel to confirm they work with relative paths.
2. Strip the personal path (`/Users/jj/...`) from all notebooks.
3. Zip, confirm the address, and send with the exact subject line.

---

## 8. Caveats on this audit

- My reruns re-implement the network from `ANN_augmented.ipynb`. They match its settings but not its random draws, so individual counts differ by an image or two.
- I could not find how 98.2% was obtained, so I have not claimed it was wrong, only that the zip does not support it.
- The rotated-test results are exploratory: 3-4 seeds and one transformation family. Treat them as a design for your own experiment.
- No marking rubric was provided; the alignment table uses the guide's stated requirements.
