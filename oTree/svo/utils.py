from math import sqrt


'''
line (a, b, c) in the form ax+by+c=0
point (x0,y0)
'''
def distance_to_line(point, line):
	a, b, c = line
	x0, y0 = point

	dist = abs(a * x0 + b * y0 + c)
	norm_term = sqrt(a ** 2 + b ** 2)

	return dist / norm_term


# stores a line using three variable A, B, C
# which represents line Ax+By=c
def compute_line(point1, point2):
	x1, y1 = point1
	x2, y2 = point2
	A = y2 - y1
	B = x1 - x2
	C = B * y1 + A * x1
	return A, B, C


def intersection_point(line1, line2):
	A1, B1, C1 = line1
	A2, B2, C2 = line2

	det = A1 * B2 - A2 * B1

	x = (B2 * C1 - B1 * C2) / det
	y = (A1 * C2 - A2 * C1) / det

	return x, y


# euclidean distance between two points
def distance(point1, point2):
	x1, y1 = point1
	x2, y2 = point2
	dist = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

	return dist

# given two points (x1, y1) and (x2, y2)
# returns that maximize the filter function
def max_tuple(point1, point2, filter_func):
	sum1 = filter_func(point1)
	sum2 = filter_func(point2)

	if sum1 >= sum2:
		return point1
	else:
		return point2
