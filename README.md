# Which EGL device am I using?

This file provides to options to see which EGL device is being used:

```
bash build.sh 			# compile c++ code
python list_egl_options.py 	# run c++ code multiple times
python egl_cuda.py          # helper function to get EGL device id from Cuda device id.
python egl_python.py		# see what the pyOpenGL default option is, requires pyOpenGL
```
