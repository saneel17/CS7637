# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

from PIL import Image, ImageChops, ImageFilter, ImageOps, ImageStat
import numpy as np
from RavensFigure import RavensFigure
from RavensProblem import RavensProblem
import time
import cv2


class Agent:
    image_a = []
    image_b = []
    image_c = []
    image_d = []  # Only for 3x3 Problems
    image_e = []  # Only for 3x3 Problems
    image_f = []  # Only for 3x3 Problems
    image_g = []  # Only for 3x3 Problems
    image_h = []  # Only for 3x3 Problems
    answer_1 = []
    answer_2 = []
    answer_3 = []
    answer_4 = []
    answer_5 = []
    answer_6 = []
    answer_7 = []  # Only for 3x3 Problems
    answer_8 = []  # Only for 3x3 Problems
    answers = []

    counter = 0

    def __init__(self):
        pass

    def Solve(self, problem):

        # if problem.problemSetName != "Basic Problems C" and problem.problemSetName != "Challenge Problems C":
        #   return 1

        self.image_a = Image.open(
            problem.figures['A'].visualFilename).convert('L')
        self.image_a = cv2.imread(problem.figures['A'].visualFilename, 0)
        self.image_a = self.Binarize_Image(self.image_a)
        self.image_b = Image.open(
            problem.figures['B'].visualFilename).convert('L')
        self.image_b = cv2.imread(problem.figures['B'].visualFilename, 0)
        self.image_b = self.Binarize_Image(self.image_b)

        self.image_c = Image.open(
            problem.figures['C'].visualFilename).convert('L')
        self.image_c = cv2.imread(problem.figures['C'].visualFilename, 0)
        self.image_c = self.Binarize_Image(self.image_c)

        if problem.problemType == "3x3":
            self.image_d = Image.open(
                problem.figures['D'].visualFilename).convert('L')
            self.image_e = Image.open(
                problem.figures['E'].visualFilename).convert('L')
            self.image_f = Image.open(
                problem.figures['F'].visualFilename).convert('L')
            self.image_g = Image.open(
                problem.figures['G'].visualFilename).convert('L')
            self.image_h = Image.open(
                problem.figures['H'].visualFilename).convert('L')
            self.image_d = cv2.imread(problem.figures['D'].visualFilename, 0)
            self.image_d = self.Binarize_Image(self.image_d)
            self.image_e = cv2.imread(problem.figures['E'].visualFilename, 0)
            self.image_e = self.Binarize_Image(self.image_e)
            self.image_f = cv2.imread(problem.figures['F'].visualFilename, 0)
            self.image_f = self.Binarize_Image(self.image_f)
            self.image_g = cv2.imread(problem.figures['G'].visualFilename, 0)
            self.image_g = self.Binarize_Image(self.image_g)
            self.image_h = cv2.imread(problem.figures['H'].visualFilename, 0)
            self.image_h = self.Binarize_Image(self.image_h)

        self.answer_1 = Image.open(
            problem.figures['1'].visualFilename).convert('L')
        self.answer_1 = cv2.imread(problem.figures['1'].visualFilename, 0)
        self.answer_1 = self.Binarize_Image(self.answer_1)

        self.answer_2 = Image.open(
            problem.figures['2'].visualFilename).convert('L')
        self.answer_2 = cv2.imread(problem.figures['2'].visualFilename, 0)
        self.answer_2 = self.Binarize_Image(self.answer_2)
        self.answer_3 = Image.open(
            problem.figures['3'].visualFilename).convert('L')
        self.answer_3 = cv2.imread(problem.figures['3'].visualFilename, 0)
        self.answer_3 = self.Binarize_Image(self.answer_3)
        self.answer_4 = Image.open(
            problem.figures['4'].visualFilename).convert('L')
        self.answer_4 = cv2.imread(problem.figures['4'].visualFilename, 0)
        self.answer_4 = self.Binarize_Image(self.answer_4)
        self.answer_5 = Image.open(
            problem.figures['5'].visualFilename).convert('L')
        self.answer_5 = cv2.imread(problem.figures['5'].visualFilename, 0)
        self.answer_5 = self.Binarize_Image(self.answer_5)
        self.answer_6 = Image.open(
            problem.figures['6'].visualFilename).convert('L')
        self.answer_6 = cv2.imread(problem.figures['6'].visualFilename, 0)
        self.answer_6 = self.Binarize_Image(self.answer_6)

        if problem.problemType == "3x3":
            self.answer_7 = Image.open(
                problem.figures['7'].visualFilename).convert('L')
            self.answer_7 = cv2.imread(problem.figures['7'].visualFilename, 0)
            self.answer_7 = self.Binarize_Image(self.answer_7)

            self.answer_8 = Image.open(
                problem.figures['8'].visualFilename).convert('L')
            self.answer_8 = cv2.imread(problem.figures['8'].visualFilename, 0)
            self.answer_8 = self.Binarize_Image(self.answer_8)

        self.answers = []
        self.answers.append(self.answer_1)
        self.answers.append(self.answer_2)
        self.answers.append(self.answer_3)
        self.answers.append(self.answer_4)
        self.answers.append(self.answer_5)
        self.answers.append(self.answer_6)

        if problem.problemType == "3x3":
            self.answers.append(self.answer_7)
            self.answers.append(self.answer_8)

        DPR_G_H = self.Calculate_DPR(self.image_g, self.image_h)
        DPR_B_C = self.Calculate_DPR(self.image_b, self.image_c)
        IPR_G_H = self.Calculate_IPR(self.image_g, self.image_h)
        IPR_B_C = self.Calculate_IPR(self.image_b, self.image_c)

        answers_list = []
        answers_list2 = []
        for i in self.answers:
            answers_list.append(self.Calculate_DPR(self.image_h, i))
            answers_list2.append(self.Calculate_IPR(self.image_h, i))

        print(problem.name, DPR_G_H, answers_list, answers_list2)
        #index = np.argmin(np.abs(answers_list-DPR_G_H))
        index = np.argmin(np.abs(answers_list-IPR_B_C))
        return index + 1

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
            similarity = self.Image_Similarity(i, image3)

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
            img_similarity = self.Image_Similarity(i, image2)
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

        # print(ImageChops.difference(image1, image2))

        matrix_3 = np.subtract(matrix_1, matrix_2)
        pixel_difference = (np.abs(matrix_3) > 127).sum()

        no_of_pixels = image1.size[0] * image1.size[1]
        similarity = 1.0 - (pixel_difference / (no_of_pixels * 1.0))

        return similarity

    def Binarize_Image(self, image):
        ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        return image

    def Calculate_DPR(self, image1, image2):
        DPR_1 = np.sum(image1)/np.size(image1)
        DPR_2 = np.sum(image2)/np.size(image2)
        return DPR_1 - DPR_2

    def Calculate_IPR(self, image1, image2):
        intersection = cv2.bitwise_or(image1, image2)
        intersection_pixels = np.sum(intersection)
        blackpixels1 = np.sum(image1)
        blackpixels2 = np.sum(image2)
        return (intersection_pixels/blackpixels1) - (intersection_pixels/blackpixels2)
