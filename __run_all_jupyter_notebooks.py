import sys, os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter

def tohtml(working_directory, input, output=None):
	prevcwd = os.getcwd()
	try:
		os.chdir(working_directory)
		
		if output is None:
			output = input + ".html"

		print("Converting %s --> %s" % (input, output))
		ep = ExecutePreprocessor(timeout=300, kernel_name='python3')

		with open(input) as f:
			nb = nbformat.read(f, as_version=4)
			
		ep.preprocess(nb, {'metadata': {'path': './'}})

		#filename_output = input + ".executed.ipynb"
		#with open(filename_output, 'wt') as f:
		#    nbformat.write(nb, f)

		exportHTML = HTMLExporter()
		(body, resources) = exportHTML.from_notebook_node(nb)

		with open(output, 'wt') as f:
			f.write(body)
		
		print("Done")
	finally:
		os.chdir(prevcwd)
	
tohtml("binomial_option_pricing", "binomial_option_pricing.ipynb")
tohtml("black_litterman", "black_litterman.ipynb")
tohtml("heath_jarrow_morton","hjm.ipynb")
tohtml("LU_decomposition","LU_decomposition.ipynb")
tohtml("principal_component_analysis","PCA.ipynb")
tohtml("time_value_of_money","tvm.ipynb")
tohtml("yield_curve_bootstrapping","bootstrapping.ipynb")