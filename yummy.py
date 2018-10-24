import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap

# yummy by Vince Petaccio

def clamp(x):
	# Clamp RGB values to be between 0 and 255 inclusive
	return int(max(0, min(x, 255)))

def rgb_to_color(r, g, b):
	# Convert decimel RGB to hex color
	return "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))

def rainbow(colors=10, f=list(np.ones(3)*2*np.pi), p=[2*np.pi/3, 4*np.pi/3, 2*np.pi], 
	center=128, width=127, reverse=False, complements=False, frac=1, cycles=False):
	"""Returns a list of colors spanning a rainbow

	Frequency, phase, center, and width of the color cycles can be specified. A single 
	rainbow, a portion of a rainbow, or multiple cycles can be specificed. 

	For pastels, try center = 210, width = 45
	Also try p = [0, 2*np.pi/3, 4*np.pi/3]
	Magenta > Purple gradient: yummy.rainbow(10, f=[1.2, 1.8, 2.5])

	Args:
		colors: Number of colors to return, default = 10
		f: List of length 3 indicating the frequencies of the red, green, and blue
			color cycles, [R, G, B], default = [2pi, 2pi, 2pi]
		p: Phase offset of the color cycles for the red, green, and blue channels,
			default = [2pi/3, 4pi/3, 2pi]
		center: Median value of each color cycle. center + width must be <= 255 and
			center - width must be >= 0, default = 128
		width: Amplitude of each sinusoidal color cycle, as deviation from center.
			center + width must be <= 255 and center - width must be >= 0, default = 127
		reverse: Flip the ordering of the colors returned, default = False
		complements: TODO: Implement tuples of complementary colors
		frac: Portion of the color cycle to return, clamped at max of 1.0, default = 1.0
		cycles: Boolean, whether to include multiple cycles of colors. Note that
			with default values of f, True will result in multiples of pi; the same
			color will be returned multiple times, default = False
	Returns:
		colors: A list of colors as hex values
	"""
	# Check the values of center and width
	assert(center + width <= 255), 'center and width must sum to 255 or less'
	assert(center - width >= 0), 'center minus width must be 0 or greater'
	# Add 1 to the number of colors and later remove to avoid seeing a color twice
	colors += 1
	# Create a list of x values
	x = 1. * np.arange(colors)
	# Normalize the x vector if there shouldn't be any cycles
	if not cycles: x = x / colors
	# Set the fraction of rainbow to be returned
	x *= np.minimum(1.0, np.abs(frac))
	# Generate the R, G, and B values using specifieid frequencies phase shifts
	red = np.sin(f[0] * x + p[0]) * width + center
	green = np.sin(f[1] * x + p[1]) * width + center
	blue = np.sin(f[2] * x + p[2]) * width + center
	# Convert the RGB values to a list of hex values
	colors = [rgb_to_color(r, g, b) for r, g, b in zip(red, green, blue)]
	# Remove the last color, since this is roughly the same color as the first
	colors.pop(-1)
	# Add support for complementary tuples
	if complements > 1:
		print('Complementary colors not yet implemented. Sorry! :[')
		pass
	# Reverse the rainbow if requested
	if reverse: colors.reverse()
	# Return the colors
	return colors

def show_colors(colors):
	# Print a color strip to show the colors selected
	fig1 = plt.figure()
	ax1 = fig1.add_subplot(111, aspect='equal')
	i = 0
	# Plot a rectangle for each color
	for c in colors:
		ax1.add_patch(patches.Rectangle((0.1 + i, 0.1), 0.5, 
			len(colors) / 5, edgecolor='none', facecolor=c))
		i += .5
	# Format the plot
	ax1.set_xlim((0, i + 0.2))
	ax1.set_ylim((0, .5 + len(colors) / 5))
	plt.tight_layout()
	plt.axis('off')
	# Display the plot
	plt.show()

def colorful_plot(x, y, colors, style='along', flip=True, return_plot=False, **kw):
	# Validate the style variable
	assert(style=='along' or style=='up'), 'style must be "along" or "up"'
	# Convert lists to NumPy arrays
	if type(y) != np.array:
		y = np.array(y, dtype=np.float64)
	else:
		if y.dtype != np.dtype('float64'):
			y = y.astype('float64')
	if type(x) != np.array:
		x = np.array(x, dtype=np.float64)
	else:
		if x.dtype != np.dtype('float64'):
			x = x.astype('float64')
	if style == 'along':
		# Color along the line
		# Ensure that the number of color and data points are equal
		while len(x) > len(colors):
			if flip:
				colors.extend(colors[::-1])
			else:
				colors.extend(colors)
		if len(colors) > len(x):
			colors = colors[:len(x)]
		# Compute pairwise distances between points to avoid compression of colors
		color_mask = np.hstack((np.zeros(1), np.sqrt(np.square(x[1:] - x[:-1]) + 
							   np.square(y[1:] - y[:-1]))))
		color_mask = np.cumsum(color_mask)
		color_mask /= np.max(color_mask)
	elif style == 'up':
		# Color up the y-axis
		# Normalize y
		color_mask = (y - np.min(y))
		color_mask /= np.max(color_mask)
	# Define a temporary custom colormap with a set of color tuples
	clrtpls = [(v, c) for v, c in zip(np.linspace(0, 1, len(colors)), colors)]
	colormap = LinearSegmentedColormap.from_list('tmp', clrtpls) 
	# Make zip objects from x and y
	x_z = zip(x[:-1], x[1:])
	y_z = zip(y[:-1], y[1:])
	# Setup the colors for plotting
	cmap = plt.get_cmap(colormap)
	# Iteratively plot all of the points with different colors
	color_plot = plt.figure()
	for x, y, c in zip(x_z, y_z, color_mask):
		plt.plot(x, y, '-', c=cmap(c), **kw)
	# Return the plot figure
	return color_plot
