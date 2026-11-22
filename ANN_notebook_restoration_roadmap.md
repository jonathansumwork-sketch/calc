# Roadmap: restoring `ANN_augmented.ipynb` to submittable quality

Scope: your own notebooks only (`ANN_augmented.ipynb`, `Baseline_training.ipynb`, your edit of the expander, and `conversion.ipynb`). The course template `RANN_finish_project.ipynb` is not part of this plan. The ready-to-paste cells in the appendix were tested against your own network class and data.

---

## 1. What "submittable" means

A marker should be able to open the notebook in any folder that holds your three CSV files, press Restart and Run All, and get the same numbers that your report quotes, with no errors, no personal file paths, and no leftovers from earlier attempts.

## 2. Where the notebook stands now

| Item | Status |
|---|---|
| Network class and training loop | Correct; identical to the course code. Do not change |
| 4x result (99.6%, 498/500) and confusion matrix | Executed and saved |
| Baseline run on the 500 original images | Exists in `Baseline_training.ipynb` (saved output 491/500 = 98.2%), but **not reproducible**: its exact code on your submitted CSV gives 411 to 447 correct over 8 seeds, never 491. See section 2b |
| Training order | The augmented CSV was shuffled once by the expander. `symbols_training.csv` is sorted by class, and `Baseline_training.ipynb` trains on it in file order with no shuffle, which scores about 86% (411 to 447/500) |
| Random seed | **None**, so numbers and errors change on every run |
| File paths | **Hard-coded `/Users/jj/...`**, so no marker can run it |
| Stale material | Header comment about MNIST, unused imports (`imageio`, `glob`), an empty last cell |
| Explanatory text | None |
| Results saved to a file | Only the confusion matrix image |

### 2b. Your baseline notebook (`Baseline_training.ipynb`)

- It uses the same network class and settings as your augmented notebook (784-200-10, learning rate 0.1, 10 epochs), loads `../symbols_training.csv` and `../symbols_testing.csv`, and saves the output 491/500 = 98.2%, which is the report's baseline.
- **It does not reproduce.** I ran its exact code on the CSV in your zip with 8 different seeds: 447, 420, 431, 438, 444, 431, 411 and 429 correct, never 491. The cause is training order: the file is sorted by class and the loop never shuffles.
- **The saved output is probably from a different state.** The saved execution counts are 1, 1, 2, 11, 12, 4, 14, 15, 16, 17, 18, so the training file was loaded at step 4, before the network was re-created at steps 11 and 12. That fits cells being run out of order, so the saved 98.2% may have come from a different or older training list in memory.
- **Consequence:** pressing Restart and Run All on this notebook would print about 86%, which would make the baseline look much worse than the augmented model for the wrong reason. Do not submit it as is.
- Other issues: no seed, the `../` path only works from a sub-folder, unused imports, a stale MNIST header, an empty last cell, and no confusion matrix.

## 3. Roadmap

### Phase 0: protect what you have (5 minutes)
1. Make a folder called `backup/` and copy into it `ANN_augmented.ipynb`, `Baseline_training.ipynb`, `expander_2026-1 (1).ipynb`, `conversion.ipynb` and the three CSV files.
2. Work on a copy named `ANN_final.ipynb`. Never edit the backups.

### Phase 1: rebuild the notebook in a clear order (30 to 45 minutes)
Merge `Baseline_training.ipynb` and `ANN_augmented.ipynb` into one notebook so both models run under the same protocol. Keep your existing neural-network class cell exactly as it is. Replace everything else with this layout:

| Order | Cell | Content |
|---|---|---|
| 1 | Markdown | Title, what the notebook does, files needed, outputs written (text in appendix B) |
| 2 | Code | Imports, folder, seed, network size, learning rate, epochs (appendix A) |
| 3 | Code | **Your unchanged `neuralNetwork` class** |
| 4 | Code | Load the three CSV files and print their sizes |
| 5 | Code | Training and testing functions |
| 6 | Code | Baseline run, augmented run, results table saved to `experiment_results.csv` |
| 7 | Code | Confusion matrices for both models, saved to `confusion_matrices.png`, plus a list of the errors |

Delete (from both notebooks): the MNIST header comment, `imageio` and `glob`, every `/Users/jj/...` path, the separate load/train/test cells that these replace, and the empty last cell.

Why each change matters:
- **Relative paths:** `Path.cwd()` means the notebook works wherever it is saved next to the CSVs.
- **Fixed seed:** the same numbers on every run, so the report can quote them.
- **Shuffle every epoch for both runs:** the same protocol for both conditions, and it protects the class-sorted baseline file.
- **A confusion matrix for both models:** the baseline errors are as informative as the augmented ones.

### Phase 2: run it and verify (20 minutes)
1. Choose Kernel, then Restart and Run All. Fix any error before moving on.
2. Check that the printed sizes are 500, 2,000 and 500.
3. Run it a second time and confirm the numbers are identical.
4. Copy the notebook and the three CSVs into a brand-new empty folder and run it there. This proves the paths work.
5. Confirm that `experiment_results.csv` and `confusion_matrices.png` appeared, and that no cell shows an error.
6. Save the notebook with its outputs showing.

Expected on my test of these cells (seed 0): baseline 498/500 and augmented 498/500, both 99.6%. Errors were 6 as 7 and 6 as 1 for the baseline, and 6 as 5 and 4 as 2 for the augmented model. If your machine gives a number differing by an image or two, use your own printed numbers, and make sure the report quotes exactly those.

### Phase 3: optional strengthening (30 minutes)
Only add what you will also discuss in the report.
- **Seed loop (recommended):** repeats both runs over several seeds so you can quote a mean and spread (appendix C). In my test of 3 seeds the two conditions matched, but one image is only 0.2 percentage points, so a mean is safer than a single run.
- **Threefold condition:** only if you want to keep that row in the report. It needs a second CSV made with the expander. If not, delete the threefold row and paragraph from the report instead.

### Phase 4: clean the expander (15 minutes)
1. Copy your edited expander into `augmentation_code/` and rename it, for example `augmentation_expander.ipynb`.
2. Replace the `/Users/jj/...` path with a relative one.
3. Fix its comment: it says three rotation values, but the code uses four (20, 10, 0, -10).
4. Add one line saying positive angles are anticlockwise.
5. Re-run it and confirm it rewrites `symbols_training_augmented.csv` with identical content. I checked that your expander logic reproduces the current file exactly, row for row (the shuffle seed is fixed at 42).
6. Delete `bigger_set.csv`, which is the same data in unshuffled order.

### Phase 5: decide what to do with `conversion.ipynb` (30 to 60 minutes)
It has 54 code cells, no explanatory text, four saved error outputs (cells 6, 9, 19 and 37, counting from 0 at the top) and hard-coded paths. The checklist does not require it. Choose one:
- **Option A (fast):** leave it out of the submission.
- **Option B (recommended if time allows):** submit a cleaned copy in `data_preparation/` containing only the final route: the automatic extraction (cell 43), the manual re-crop of `7_0073` (cells 45 to 48, which must stay together), the count check (cell 49) and the split and CSV writing (cell 50). Add a short note at the top, use relative paths, and mention in the report that one image was re-cropped by hand.

### Phase 6: package (20 minutes)
Final folder:

| Include | Notes |
|---|---|
| `symbols_training.csv`, `symbols_training_augmented.csv`, `symbols_testing.csv` | Required |
| `ANN_final.ipynb` (executed) | Required |
| `augmentation_code/augmentation_expander.ipynb` | Required (augmentation code) |
| `data_preparation/` (if you did option B) | Optional |
| Report `.docx` with the visual abstract | Required |

Remove: `RANN_finish_project.ipynb` (course template), `ANN_augmented.ipynb`, `.ipynb_checkpoints/`, `.DS_Store`, `qc_backups/`, the superseded image folders, practice CSVs, `bigger_set.csv` and the course repo folder. Zip, unzip somewhere else, and run `ANN_final.ipynb` once more from there.

## 4. Acceptance checklist
- [ ] Restart and Run All completes with no errors
- [ ] Two consecutive runs print identical numbers
- [ ] The notebook runs from a fresh folder with only the three CSVs
- [ ] No `/Users/...` path appears anywhere in submitted files
- [ ] Baseline and augmented use the same network, seed, epochs and shuffling
- [ ] Both confusion matrices and `experiment_results.csv` are saved
- [ ] Every number in the report appears in the printed output
- [ ] The report's methods match the notebook (200 hidden nodes, 10 epochs, learning rate 0.1, rotations -10, 0, +10, +20)

## 5. Effect on the report
The report's 98.2% baseline comes from `Baseline_training.ipynb`, whose output does not reproduce on your submitted data. Once both models are run under the same shuffled, seeded protocol, replace the baseline figure with the printed number. If it lands near 99.6% as in my test, the claimed improvement from 98.2% to 99.6% will not hold, and Results and Discussion need rewriting around "no clear difference". The threefold 99.4% still has no notebook; if you have one, send it and I will check it, otherwise remove that row and its paragraph. Do the notebook first, then update the report.

---

## Appendix A: ready-to-paste cells (tested)

Paste these in place of your old load, train and test cells. Cell 3 is your unchanged `neuralNetwork` class.

### Cell 2 (code): imports, folder, settings

```
from pathlib import Path
import csv, random
import numpy
import scipy.special
import matplotlib.pyplot

project = Path.cwd()          # run the notebook from the folder that holds the CSV files
SEED = 0                      # fixed seed, so every run gives the same numbers

input_nodes, hidden_nodes, output_nodes = 784, 200, 10
learning_rate = 0.1
epochs = 10
```

### Cell 4 (code): load the data

```
def load_lines(filename):
    with open(project / filename, "r") as f:
        return f.readlines()

training_data_list  = load_lines("symbols_training.csv")            # 500 original training images
augmented_data_list = load_lines("symbols_training_augmented.csv")  # 2,000 images (originals + rotations)
testing_data_list   = load_lines("symbols_testing.csv")             # 500 original test images, never augmented
print("Training:", len(training_data_list), " Augmented:", len(augmented_data_list), " Testing:", len(testing_data_list))
```

### Cell 5 (code): training and testing functions

```
def prepare(record):
    all_values = record.split(',')
    inputs = (numpy.asarray(all_values[1:], dtype=float) / 255.0 * 0.99) + 0.01
    return int(all_values[0]), inputs

def train_network(data_list, seed=SEED):
    random.seed(seed)
    numpy.random.seed(seed)                          # same seed -> same starting weights
    net = neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)
    data = list(data_list)
    for e in range(epochs):
        random.shuffle(data)                         # new order every epoch (the training CSV is sorted by class)
        for record in data:
            label, inputs = prepare(record)
            targets = numpy.zeros(output_nodes) + 0.01
            targets[label] = 0.99
            net.train(inputs, targets)
    return net

def test_network(net, data_list):
    confusion = numpy.zeros((10, 10), dtype=int)     # rows = actual symbol, columns = predicted symbol
    for record in data_list:
        label, inputs = prepare(record)
        confusion[label, numpy.argmax(net.query(inputs))] += 1
    return confusion
```

### Cell 6 (code): baseline and augmented runs, results table

```
baseline_net  = train_network(training_data_list)
augmented_net = train_network(augmented_data_list)
cm_baseline  = test_network(baseline_net,  testing_data_list)
cm_augmented = test_network(augmented_net, testing_data_list)

results = []
for name, n_train, cm in [("Baseline (original images)", len(training_data_list), cm_baseline),
                          ("Augmented (4x)", len(augmented_data_list), cm_augmented)]:
    correct = int(numpy.trace(cm))
    results.append([name, n_train, len(testing_data_list), hidden_nodes, learning_rate, epochs, SEED, correct, correct / len(testing_data_list) * 100])
    print(f"{name}: {n_train} training images, {correct}/{len(testing_data_list)} correct, accuracy {correct / len(testing_data_list) * 100:.1f}%")

with open(project / "experiment_results.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Condition", "Training images", "Test images", "Hidden nodes", "Learning rate", "Epochs", "Seed", "Correct", "Test accuracy (%)"])
    w.writerows(results)
```

### Cell 7 (code): confusion matrices and error list

```
fig, axs = matplotlib.pyplot.subplots(1, 2, figsize=(11, 4.7))
for ax, cm, title in [(axs[0], cm_baseline, "Baseline"), (axs[1], cm_augmented, "Augmented (4x)")]:
    ax.imshow(cm, cmap="Blues", vmin=0)
    ax.set_title(title); ax.set_xlabel("Predicted symbol"); ax.set_ylabel("Actual symbol")
    ax.set_xticks(range(10)); ax.set_yticks(range(10))
    for i in range(10):
        for j in range(10):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center", fontsize=8, color="white" if cm[i, j] > 25 else "black")
fig.tight_layout()
fig.savefig(project / "confusion_matrices.png", dpi=300, bbox_inches="tight")
matplotlib.pyplot.show()

for name, cm in [("Baseline", cm_baseline), ("Augmented", cm_augmented)]:
    errors = [(int(cm[i, j]), i, j) for i in range(10) for j in range(10) if i != j and cm[i, j] > 0]
    print(name, "errors (actual -> predicted, count):", [f"{i}->{j} x{n}" for n, i, j in sorted(errors, reverse=True)])
```


## Appendix B: markdown text for cell 1

```
# Symbol lexicon: baseline vs augmented ANN

Trains the course ANN (784-200-10, sigmoid, learning rate 0.1, 10 epochs) on (a) the 500 original
training images and (b) the 2,000-image augmented set (the originals plus rotations of -10, +10
and +20 degrees), then tests both on the same 500 untouched test images.

Files needed in this folder: symbols_training.csv, symbols_training_augmented.csv, symbols_testing.csv
Files written: experiment_results.csv, confusion_matrices.png
Both models use the same seed, and training order is reshuffled every epoch.
```

## Appendix C: optional seed loop (tested)

```
seeds = range(5)
base_scores, aug_scores = [], []
for s in seeds:
    base_scores.append(int(numpy.trace(test_network(train_network(training_data_list, seed=s), testing_data_list))))
    aug_scores.append(int(numpy.trace(test_network(train_network(augmented_data_list, seed=s), testing_data_list))))
print("Baseline  correct /500 per seed:", base_scores, " mean", numpy.mean(base_scores))
print("Augmented correct /500 per seed:", aug_scores,  " mean", numpy.mean(aug_scores))
```

It prints no per-epoch lines. Expect a few tens of seconds per seed on a typical laptop.
