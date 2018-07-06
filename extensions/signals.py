from blinker import Namespace


custom_signals = Namespace()

report_sent = custom_signals.signal("report_sent")
report_checked = custom_signals.signal("report_checked")
