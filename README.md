# FFR-Toolkit

Frequency-Following Response toolkit containing various DAQ, online/offline analysis toolkits and database (MongoDB). Required libraries:


# Demo

> python3 bin/FFR.py

# Visualize patient FFR

> python3 bin/FFR.py PATH_TO_FFR/Meta_AVG_data.json

# Class usage

> from ffrgui.utilities import FFRJSON
> ffr = FFRJSON.FFRJSON()

## Load path to FFR
> path = "sample/202692/Harmonique_LE85dB/Meta_AVG_data.json"
> ffr.load_path(path)

## Get FFR sepctral component waveforms
> waveforms = ffr.load_AVG()

## Get patient data
> patient_data = ffr.load_metadata()
