# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image, ImageChops, ImageFilter, ImageOps, ImageStat
import numpy as np
from RavensFigure import RavensFigure
from RavensProblem import RavensProblem
import time


class Agent:
    image_a = []
    image_b = []
    image_c = []
    answer_1 = []
    answer_2 = []
    answer_3 = []
    answer_4 = []
    answer_5 = []
    answer_6 = []
    answers = []
    counter = 0

    def __init__(self):
        pass

    def Solve(self, problem):

        if problem.name != "Basic Problem B-06":
            return 1

        # print(problem.name)
        self.image_a = Image.open(
            problem.figures['A'].visualFilename).convert('L')
        # print(self.image_a.size) (184,184)
        # print(self.image_a.mode) (RGB)
        self.image_b = Image.open(
            problem.figures['B'].visualFilename).convert('L')
        self.image_c = Image.open(
            problem.figures['C'].visualFilename).convert('L')

        self.answer_1 = Image.open(
            problem.figures['1'].visualFilename).convert('L')
        self.answer_2 = Image.open(
            problem.figures['2'].visualFilename).convert('L')
        self.answer_3 = Image.open(
            problem.figures['3'].visualFilename).convert('L')
        self.answer_4 = Image.open(
            problem.figures['4'].visualFilename).convert('L')
        self.answer_5 = Image.open(
            problem.figures['5'].visualFilename).convert('L')
        self.answer_6 = Image.open(
            problem.figures['6'].visualFilename).convert('L')

        self.answers = []
        self.answers.append(self.answer_1)
        self.answers.append(self.answer_2)
        self.answers.append(self.answer_3)
        self.answers.append(self.answer_4)
        self.answers.append(self.answer_5)
        self.answers.append(self.answer_6)

        # Check Across Row
        index_1, similarity_score_1 = self.Compare_Images_2x2(
            self.image_a, self.image_b)
        # Check Across Column
        index_2, similarity_score_2 = self.Compare_Images_2x2(
            self.image_a, self.image_c)
        # If checked accross row, then apply transformation to Image C.
        transformation_3_list1 = self.Apply_Base_Transformations(
            self.image_c)
        # If checked accross column, then apply transformation to Image B.
        transformation_3_list2 = self.Apply_Base_Transformations(
            self.image_b)

        if similarity_score_1 > similarity_score_2:
            image3 = transformation_3_list1[index_1]
        else:
            image3 = transformation_3_list2[index_2]

        # transformation_3_list2[4].show()
        self.counter = 1
        max_similarity = 0
        to_return = 0

        for i in self.answers:
            similarity = self.Calculate_Tversky(i, image3)

            if similarity > max_similarity:
                max_similarity = similarity
                to_return = self.counter
            self.counter = self.counter + 1

        return to_return

    def Apply_Base_Transformations(self, image):
        '''
        Returns a list of 8 transformations
        '''
        transformations = []
        angle = [90, 180, 270]
        for i in angle:
            transformations.append(image.rotate(i))
        for i in angle:
            transformations.append(ImageOps.flip(image.rotate(i)))
        transformations.append(ImageOps.flip(image))
        transformations.append(image)
        return transformations

    def Compare_Images_2x2(self, image1, image2):
        '''
        Compares images for a 2 x 2 problem and returns the similarity score
        '''
        transformations = []
        transformations = self.Apply_Base_Transformations(image1)
        max_similarity = 0
        counter = 0
        toreturn = 0
        for i in transformations:
            img_similarity = self.Calculate_Tversky(i, image2)
            # i.show()
            # print(img_similarity)
            # time.sleep(1)
            if img_similarity >= max_similarity:
                max_similarity = img_similarity
                toreturn = counter
            counter = counter + 1
        # print(toreturn)
        # print(max_similarity)
        return toreturn, max_similarity

    def Image_Similarity(self, image1, image2):
        matrix_1 = np.matrix(image1).astype(float)
        matrix_2 = np.matrix(image2).astype(float)

        #print(ImageChops.difference(image1, image2))

        matrix_3 = np.subtract(matrix_1, matrix_2)
        pixel_difference = (np.abs(matrix_3) > 127).sum()

        no_of_pixels = image1.size[0] * image1.size[1]
        similarity = 1.0 - (pixel_difference / (no_of_pixels * 1.0))

        return similarity

    def Calculate_Tversky(self, img1, img2):
        similarity = len(np.where((img1 == 0) & (img2 == 0))[0])/(len(np.where((img1 == 0) & (
            img2 == 0))[0]) + len(np.where((img1 == 0))[0]) + len(np.where((img2 == 0))[0]))
        # print(similarity)
        return similarity
