
# SOURCE POUR LE SCRIPT PARSING_V2
# Pour reload le package 
# imp.reload(source)

import numpy as np 
# Color Function

def hex_to_RGB(hex):
  ''' "#FFFFFF" -> [255,255,255] '''
  # Pass 16 to the integer function for change of base
  return [int(hex[i:i+2], 16) for i in range(1,6,2)]

def color_dict(gradient):
  ''' Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on '''
  return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
      "r":[RGB[0] for RGB in gradient],
      "g":[RGB[1] for RGB in gradient],
      "b":[RGB[2] for RGB in gradient]}  


def RGB_to_hex(RGB):
  ''' [255,255,255] -> "#FFFFFF" '''
  # Components need to be integers for hex to make sense
  RGB = [int(x) for x in RGB]
  return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])


def linear_gradient(start_hex="#000000", finish_hex="#ff0000", n=10):
  ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") '''
  # Starting and ending colors in RGB form
  s = hex_to_RGB(start_hex)
  f = hex_to_RGB(finish_hex)
  # Initilize a list of the output colors with the starting color
  RGB_list = [s]
  # Calcuate a color at each evenly spaced value of t from 1 to n
  for t in range(1, n):
    # Interpolate RGB vector for color at the current value of t
    curr_vector = [
      int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
      for j in range(3)
    ]
    # Add it to our list of output colors
    RGB_list.append(curr_vector)

  return color_dict(RGB_list)


# PytagCloug Custom 

def defscale(count, mincount, maxcount, minsize, maxsize):
    if maxcount == mincount:
        return int((maxsize - minsize) / 2.0 + minsize)
    return int(minsize + (maxsize - minsize) * 
               (count * 1.0 / (maxcount - mincount)) ** 0.8)



def my_make_tags(wordcounts, minsize=3, maxsize=36, colors=None, scalef=defscale, color="#000000"):
	"""
	sizes and colors tags 
	wordcounts is a list of tuples(tags, count). (e.g. how often the
	word appears in a text)
	the tags are assigned sizes between minsize and maxsize, the function used
	is determined by scalef (default: square root)
	color is either chosen from colors (list of rgb tuples) if provided or random
	"""
	counts = [tag[1] for tag in wordcounts]

	if not len(counts):
		return []

	maxcount = max(counts)
	mincount = min(counts)

	distinct_value = len(np.unique(counts))
	index_value = sorted(np.unique(counts))

	colors = linear_gradient("#000000", n = distinct_value )

	tags = []
	for word_count in wordcounts:

		index = index_value.index(word_count[1])
		color = (colors["r"][index], colors["g"][index], colors["g"][index] )

		tags.append({'color': color, 'size': scalef(word_count[1], mincount,
													maxcount, minsize, maxsize),
					 'tag': word_count[0]})
	return tags, colors
