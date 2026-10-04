########## EVA ##########
'''
EVA - Eva Virtual Assistant (ARS Mk1.0)
Part of the Agent Runtime Environment Architecture (Project AREA)
Copyright (c) 2026
- LivelyCoffee and Team
'''
#########################

# ---------- MAIN ENTRY-POINT ----------

from .bootstrap import bootstrap

if __name__ == "__main__":
    runtime = bootstrap()
    try:
        runtime.start()
    finally:
        runtime.stop()

#*---------- END OF CODE ----------*

########## DEVELOPER FOOTER ##########

# This is a work in progress experimental project, 
# not intended for public release anytime soon.
# Please excercise caution!

######################################
