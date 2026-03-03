setup:
	pip install pandas numpy pyarrow

preproc:
	python preproc.py

compute:
	python src.py

cleanup:
	-del /f grid_arrays.pkl grid_params.json grid_data.json grid_data.parquet