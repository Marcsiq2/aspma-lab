# Marc Siquier Peñafort ASPMA LAB SESSIONS 2-3
## Task 2: Agreement between AcousticBrainz vs MS data

### AB bpm vs MSD tempo
Consider two evaluation metrics:
* Accuracy 1: The percentage of AB bpm estimates within 4% (the precision window) of the MSD tempo.
* Accuracy 2: The percentage of AB bpm estimates within 4% of either the MSD tempo, or half, double, three times, or one third of the MSD tempo. 

### AB danceability vs MSD danceability
* Use Pearson correlation (scipy) and Maximal information coefficient (minepy)

### AB beats_position vs MSD beats_start
* consider different confidence levels provided by MSD (beats_confidence) in evaluation
* use [mir_eval library](https://craffel.github.io/mir_eval/#module-mir_eval.beat)

### AB key_key/key_scale vs key/mode
* consider different confidence levels provided by MSD (key_confidence, mode_confidence) in evaluation
* use [mir_eval library](https://craffel.github.io/mir_eval/#module-mir_eval.key)
