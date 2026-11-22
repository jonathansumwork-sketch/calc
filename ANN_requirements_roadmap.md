# NEUR30006 final project: requirements checklist and roadmap

This covers two sets of expectations: (A) the instructions inside `RANN_finish_project.ipynb`, and (B) the course student guide. It is paired with `RANN_finish_project_edited.ipynb`, which implements the experiment side of the plan.

---

## 1. What the edited notebook already does

| Requirement | How the edited notebook meets it |
|---|---|
| Use `symbols_training.csv` and `symbols_testing.csv`; never augment the test set | Loads both, asserts shapes, class balance and pixel range; the test set is only ever scored, never trained on |
| Course-style ANN: 784 inputs, one hidden layer, 10 outputs, sigmoid, no bias, one image per update | Same class as the course code (weight scaling uses the input-node count, as the course code does) |
| Settings consistent with the report | 200 hidden nodes, learning rate 0.1, 10 epochs |
| Augmentation matches the submitted data | Rebuilds the 4x set (-10, 0, +10, +20 degrees) from the training CSV and asserts it is identical to `symbols_training_augmented.csv`; the submitted file is never overwritten |
| Threefold condition documented | Builds the 3x set (0, +10, +20) in code and saves it to `outputs/symbols_training_augmented_3x.csv` |
| Fair comparison | Shuffles training order every epoch; same seeds for every condition; 10 seeds; mean, SD, range and paired difference vs baseline |
| Separates "more updates" from "more varied images" | Control: baseline trained for 40 epochs (same number of weight updates as 4x) |
| Baseline records: accuracy, training count, classes, hyperparameters, epochs | Printed and saved in `experiment_results.csv` and `seed_results.csv` |
| Results usable for the Discussion | Confusion matrices, per-class accuracy, the test images misclassified most often, and a secondary rotation-robustness analysis |
| Executed notebook plus result files and figures | Outputs saved in `outputs/` (CSV files and figures 1-6) |
| No hard-coded personal paths | Looks for the CSVs in the current folder, its parent, or the Desktop project folder |

---

## 1b. What my executed run of the notebook showed

These come from running the edited notebook end to end (10 seeds per condition, results identical on a second run). **Reproduce them on your own machine before quoting anything in the report.**

Untouched test set (500 images; one image = 0.2 percentage points):

| Condition | Training images | Mean correct /500 (SD) | Mean accuracy |
|---|---|---|---|
| Baseline | 500 | 497.7 (0.48) | 99.54% |
| 3x rotation (0, +10, +20) | 1,500 | 496.4 (0.52) | 99.28% |
| 4x rotation (-10, 0, +10, +20) | 2,000 | 497.7 (0.48) | 99.54% |
| Control: baseline, 40 epochs | 500 | 499.0 (0.00) | 99.80% |
| Exploratory: 5x symmetric (-20 to +20) | 2,500 | 497.6 (0.70) | 99.52% |

Rotated copies of the test images (secondary analysis, mean accuracy %):

| Condition | -30 | -20 | -10 | 0 | +10 | +20 | +30 |
|---|---|---|---|---|---|---|---|
| Baseline | 48.6 | 82.6 | 98.2 | 99.5 | 98.8 | 80.6 | 55.5 |
| 3x | 30.2 | 60.7 | 95.9 | 99.3 | 99.7 | 99.6 | 93.9 |
| 4x | 58.1 | 94.3 | 99.4 | 99.5 | 99.5 | 99.2 | 91.5 |
| Control (40 epochs) | 46.1 | 81.3 | 98.4 | 99.8 | 98.6 | 76.8 | 53.6 |
| 5x symmetric | 92.3 | 99.2 | 99.5 | 99.5 | 99.4 | 98.9 | 89.9 |

What this means for the plan:
- **No clean-test gain.** Baseline and 4x are tied, 3x is slightly lower, and the 40-epoch control is highest. The report's 98.2% baseline and its claimed improvement will not survive, so Results and Discussion must be rewritten around these numbers.
- **Augmentation does change rotation robustness**, and the benefit follows the training range: 4x is strong on the +20 side but weak at -30, while the symmetric set is strong on both sides. The control shows this is not just extra training.
- **The errors are specific images, not systematic class confusion.** The 4x model gets test image 237 (a 4, predicted as 2) wrong in all 10 seeds, and test image 345 (a 6) wrong in all 10 seeds, as does the baseline. These images are shown in figure 5, which is the evidence to examine for the Discussion. The report's earlier 6 as 7 error was one seed's outcome; across seeds the 4x model's 6 errors go mostly to 5.

---

## 2. Requirements the notebook cannot meet for you

| Requirement (source) | Status | What you need to do |
|---|---|---|
| Report in 1,500 words (guide) | Needs rewriting | Rewrite Results and Discussion from the notebook's printed numbers; see section 3 |
| Introduction: design principles, assumptions, expected confusions (guide) | Partial | Say why each design choice was made; state the hypothesis and where you expect confusion |
| Methods: preprocessing, split, changes to the standard code (guide) | Missing | Add the items in section 3 |
| Justify the augmentation choice (guide) | Missing | Justify rotation-only (the preprocessing already normalises position and scale) and justify the -10 to +20 range, or use the symmetric exploratory condition |
| Discussion explains the design / augmentation / ANN interaction (guide) | Weakest part | Use the misclassified-image figure and the robustness analysis to explain *why* particular pairs are confused |
| Visual abstract (guide checklist) | Done in the earlier revision | Rebuild it once the final numbers are in |
| Notes in the old notebook about "different sizes/stroke thicknesses" | Unsupported | Drop it; each drawing was rescaled to fit about 20-21 px and centred |
| Execute on your machine and keep outputs | Needed | Run all cells from a fresh kernel in your own project folder and submit that executed copy |
| Clean submission package (guide) | Needed | See section 4 |

---

## 3. Roadmap

### Phase 1: run and check the notebook (about 30-45 minutes of waiting, 15 minutes of work)
1. Copy `RANN_finish_project_edited.ipynb` into your project folder (next to the three CSVs).
2. Run all cells from a fresh kernel. It takes roughly 10 minutes.
3. Confirm the printed line "Rebuilt 4x set identical to submitted file: True".
4. Open the `outputs/` folder and check that the numbers on screen match `experiment_results.csv`.
5. Keep this executed copy as the version you submit.

### Phase 2: decide what the evidence says (about 1 hour)
1. Compare condition means with the seed-to-seed SD. One test image is 0.2 percentage points, so a difference smaller than the SD is not a measurable effect.
2. Read the control row (baseline, 40 epochs): if it matches or beats the augmented conditions, the apparent gains came from extra training, not from image variety.
3. Look at figure 5 (misclassified test images) and write down what you actually see for each recurring error.
4. Read the rotation-robustness table: it shows what augmentation changes when the clean test set is too easy.
5. Decide how to justify the angle range, or report the exploratory symmetric condition alongside it.

### Phase 3: rewrite the report (about 3 hours, 1,500 words maximum)
Suggested budget:

| Section | Words | Must contain |
|---|---|---|
| Introduction | about 250 | Design principles; why rotation; hypothesis; expected confusions |
| Methods | about 300 | Goodnotes drawing; PDF rendering; crop, resize to fit 22x22, centre on 28x28, invert to light-on-dark; stratified random split (seed 42); ANN settings; shuffling each epoch; 10 seeds; rotation implementation (bilinear, anticlockwise positive); the 3x and 4x sets; the 40-epoch control |
| Results | about 300 | One table with mean +/- SD per condition; one confusion matrix; the robustness figure |
| Discussion | about 550 | Effect of augmentation vs a ceiling near 100%; the recurring misclassifications and why; asymmetry of the angle range; design lessons; limitations (one drawer, sequential same-session drawings, 500 test images, one augmentation type) |
| Captions and conclusion | about 100 | |

Rules: every number must come from the printed notebook output; report the baseline exactly as produced, even if augmentation does not help; keep the robustness analysis labelled as secondary.

### Phase 4: rebuild the visual abstract (about 30 minutes)
Replace the accuracy panel with the final table values and keep the same layout.

### Phase 5: package and submit (about 1 hour)
Keep only:
- `symbols_training.csv`, `symbols_testing.csv`, `symbols_training_augmented.csv`
- the executed `RANN_finish_project_edited.ipynb` and its `outputs/` folder
- the augmentation code (the notebook cells cover this; the course expander notebook produced the same file)
- the report `.docx`, with the visual abstract

Remove: `RANN_finish_project.ipynb` (the old, contradictory version), `.ipynb_checkpoints/`, `.DS_Store`, `qc_backups/`, superseded image folders, practice CSVs, `bigger_set.csv` (a duplicate of the augmented file) and the course repo folder. The source PDFs and `input_images_auto_review/` are optional provenance.

Zip it and email it with the exact subject `final_project NEUR30006`. The guide gives the address as `pkitc@unimelb.edu`, which looks truncated, so confirm it first.

---

## 4. Final self-check

- [ ] The executed notebook was run top to bottom with no errors
- [ ] "Identical to submitted file: True" is printed
- [ ] Every number in the report appears in the notebook output
- [ ] Word count is 1,500 or fewer
- [ ] Visual abstract matches the final numbers
- [ ] No `/Users/...` paths anywhere in the submitted files
- [ ] Subject line is exactly `final_project NEUR30006`
