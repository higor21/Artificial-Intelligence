
def vects_equal(vect1, vect2):
	return vect2[vect1.index(max(vect1))] == [1]

ll = [[1.2], [5.6], [2.4], [2.4]]
l2 = [[0.],[0.],[0.],[1.]]

print(vects_equal(ll,l2))