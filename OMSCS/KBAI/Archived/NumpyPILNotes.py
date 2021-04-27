import numpy as np
from PIL import Image

print(np.__version__)

a = np.array([1, 2, 3])
print(a)
print(a.shape)
print(a.dtype)
print(a.ndim)
print(a.size)
print(a.itemsize)

print(a[0])
a[0] = 10
print(a)

l = [1, 2, 3]  # Python List
a = np.array([1, 2, 3])  # Numpy Arrray
a = a + np.array([4])
a = a * 2
a = np.log(a)
print(a)


# Dot Product - Sum of products of the corresponding entries
l1 = [1, 2, 3]
l2 = [4, 5, 6]
a1 = np.array(l1)
a2 = np.array(l2)

dot = 0
for i in range(len(l1)):
    dot += l1[i] + l2[i]
print(dot)

dot = np.dot(a1, a2)

# Multi Dimensional Arrays
a = np.array([[1, 2], [3, 4]])

print(a[0][0])  # same as
print(a[0, 0])

print(a[:, 0])  # All the rows, column 0
print(a[0, :])  # Row 0, all the columns

print(a.T)
print(np.linalg.inv(a))
print(np.diag(a))

# Slicing
a = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
print(a)

# Integer Indexing
b = a[0, :]  # Row 0, All Columns
b = a[0, 1:3]  # Row 0, Columns 1 to 3, excluding 3
b = a[:, 1]
b = a[-1, -1]  # Start from the last row, from the last column.

print(b)

# Boolean Indexing
a = np.array([[1, 2], [3, 4], [5, 6]])
bool_idx = a > 2
print(bool_idx)
print(a[a > 2])  # Prints indices only if it meets the condition.

b = np.where(a > 2, a, -1)
print(b)

a = np.array([10, 19, 39, 12, 12])
b = [1, 3, 4]
print(a[b])  # Fancy Indexing
even = np.argwhere(a % 2 == 0)
print(even.flatten())

# Reshaping
a = np.arange(1, 7)  # creates a range
print(a)
print(a.shape)
b = a.reshape((2, 3))  # Reshapes it into 2 rows and 3 columns
print(b.shape)

# Concentenation
a = np.array([[1, 2], [3, 4]])
print(a)
b = np.array([[5, 6]])
c = np.concatenate((a, b), axis=None)

# Hstack - Stack arrays in sequence column-wise
a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])

c = np.vstack((a, b))
c = np.hstack((a, b))

print(c)

# Broadcasting
x = np.array([[1, 2, 3], [4, 5, 6], [1, 2, 3], [4, 5, 6]])
a = np.array([1, 0, 1])
y = x + a
print(y)

# Data Science functions and Axis
a = np.array([[7, 8, 9, 13, 10, 11, 12], [17, 18, 19, 20, 21, 22, 34]])
print(a)
print(a.sum(axis=0))  # None is default, will calculate the overall sum
print(a.sum(axis=1))  # Over the Rows
print(a.mean(axis=None))
print(a.std(axis=None))
print(a.min(axis=None))
print(a.max(axis=None))

# Datatypes
x = np.array([1, 2])
print(x.dtype)

x = np.array([1, 2, 3])
b = a  # Copying the reference
b = a.copy()

# Initialiing Arrays
a = np.zeros((2, 3))
print(a)

a = np.ones((2, 3))
print(a)

a = np.full((2, 3), 5.0)  # Full matrices of the number
print(a)

a = np.eye((3))  # Identity Matrix
print(a)

a = np.arange(20)

a = np.linspace(0, 15, 5)  # Start, stop

#a = np.random.random((3, 2))

# Pillow
image = Image.open("/Users/zulyang/OMSCS/KBAI/dog1.jpg")
image2 = Image.open("/Users/zulyang/OMSCS/KBAI/dog2.jpg")

# Properties
# For Numpy, it is usually rows and then columns. But for PIL is columns and then rows
print(image.size)
#Width, Height
print(image.format)
print(image.mode)

image.save("newimage.jpg")

# Cropping an image
left = 50
top = 120
right = 250
bottom = 230
crop_image = image.crop((left, top, right, bottom))

# Copying an image
copied_image = image.copy()

# Transposing (Changing orientation of an image)
transpose_image1 = image.transpose(Image.FLIP_LEFT_RIGHT)
transpose_image2 = image.transpose(Image.FLIP_TOP_BOTTOM)
transpose_image3 = image.transpose(Image.ROTATE_180)
transpose_image4 = image.transpose(Image.ROTATE_270)
transpose_image5 = image.transpose(Image.ROTATE_90)

# Resizing / Interpolation Techniques
newsize = (300, 300)
resized_image1 = image.resize(newsize, Image.BILINEAR)
resized_image2 = image.resize(newsize, Image.NEAREST)

# Rotation
angle = 30
rotated_image = image.rotate(angle)
rotated_image.show()
