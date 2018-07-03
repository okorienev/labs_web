from blinker import Namespace


custom_signals = Namespace()

drop_marks_cache_sig = custom_signals.signal("drop-marks-cache")  # drop group stats in course
drop_unchecked_count_cache_sig = custom_signals.signal("drop-unchecked-count-cache")  # drop count of unchecked labs
