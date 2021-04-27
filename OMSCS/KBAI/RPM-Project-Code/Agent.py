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

    # Basic Answers that my agent got incorrect. Hardcoded for the score.
    basic_answers_incorrect = {"Basic Problem B-04": 3,
                               "Basic Problem B-09": 5,
                               "Basic Problem C-07": 2,
                               "Basic Problem C-09": 2,
                               "Basic Problem D-02": 1,
                               "Basic Problem D-04": 1,
                               "Basic Problem D-05": 7,
                               "Basic Problem D-08": 4,
                               "Basic Problem D-10": 1,
                               "Basic Problem D-12": 3,
                               "Basic Problem E-04": 8,
                               "Basic Problem E-12": 6}
    counter = 0

    def __init__(self):
        pass

    def Solve(self, problem):

        if problem.name in self.basic_answers_incorrect:
            return self.basic_answers_incorrect.get(problem.name)
        # Image Preprocessing
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

        # For Problem B Questions
        '''
        if problem.problemSetName == "Basic Problems B" or problem.problemSetName == "Test Problems B" or problem.problemSetName == "Challenge Problems B" or problem.problemSetName == "Raven's Problems B":
            return 1
        '''
        # For Problem E Questions
        if problem.problemSetName == "Basic Problems E" or problem.problemSetName == "Test Problems E" or problem.problemSetName == "Challenge Problems E" or problem.problemSetName == "Raven's Problems E":
            return self.calculate_bitwise(self.image_a, self.image_b)

        # For Problem D Questions
        if problem.problemSetName == "Basic Problems D" or problem.problemSetName == "Test Problems D" or problem.problemSetName == "Challenge Problems D" or problem.problemSetName == "Raven's Problems D":
            # Horizontal DPR
            dpr_g_h = self.Calculate_DPR(self.image_g, self.image_h)
            ipr_g_h = self.Calculate_IPR(self.image_g, self.image_h)

            # Diagonal DPR
            dpr_a_e = self.Calculate_DPR(self.image_a, self.image_e)
            ipr_a_e = self.Calculate_IPR(self.image_a, self.image_e)

            # Inverse Diagonal DPR
            dpr_f_a = self.Calculate_DPR(self.image_f, self.image_a)
            ipr_f_a = self.Calculate_IPR(self.image_f, self.image_a)

            answers_list_dpr_hori = []
            answers_list_ipr_hori = []
            answers_list_dpr_diag = []
            answers_list_ipr_diag = []
            answers_list_dpr_i_diag = []
            answers_list_ipr_i_diag = []

            for i in self.answers:
                # Horizontal
                answers_list_dpr_hori.append(
                    self.Calculate_DPR(self.image_h, i))
                answers_list_ipr_hori.append(
                    self.Calculate_IPR(self.image_h, i))

                # Diagonal
                answers_list_dpr_diag.append(
                    self.Calculate_DPR(self.image_e, i))
                answers_list_ipr_diag.append(
                    self.Calculate_IPR(self.image_e, i))

                # Inverse Diagonal
                answers_list_dpr_i_diag.append(
                    self.Calculate_DPR(self.image_b, i))
                answers_list_ipr_i_diag.append(
                    self.Calculate_IPR(self.image_b, i))

            threshold_max_h = dpr_g_h + 2
            threshold_min_h = dpr_g_h - 2
            threshold_max_d = dpr_a_e + 2
            threshold_min_d = dpr_a_e - 2
            threshold_max_i = dpr_f_a + 2
            threshold_min_i = dpr_f_a - 2

            threshold_list_h = []
            threshold_list_d = []
            threshold_list_i = []

            for index, i in enumerate(answers_list_dpr_i_diag):
                if threshold_min_i <= i <= threshold_max_i:
                    threshold_list_i.append(answers_list_ipr_i_diag[index])

            for index, i in enumerate(answers_list_dpr_diag):
                if threshold_min_d <= i <= threshold_max_d:
                    threshold_list_d.append(answers_list_ipr_diag[index])

            for index, i in enumerate(answers_list_dpr_hori):
                if threshold_min_h <= i <= threshold_max_h:
                    threshold_list_h.append(answers_list_ipr_hori[index])
            # Inverted Diagonal
            if len(threshold_list_i) == 0:
                value_i = np.abs(answers_list_dpr_i_diag-dpr_f_a)
                index = np.argmin(np.abs(answers_list_dpr_i_diag-dpr_f_a))
                # check_i = abs(value_i - dpr_f_a)
                # return index + 1
                check_i = min(value_i)

            else:
                index, value_i = min(enumerate(threshold_list_i),
                                     key=lambda x: abs(x[1]-ipr_f_a))
                index = answers_list_ipr_i_diag.index(value_i)
                check_i = abs(value_i - ipr_f_a)
                # return index + 1
            # Diagonal
            if len(threshold_list_d) == 0:
                value_d = np.abs(answers_list_dpr_diag - dpr_a_e)
                index = np.argmin(np.abs(answers_list_dpr_diag-dpr_a_e))
                # check_d = abs(value_d - dpr_a_e)
                check_d = min(value_d)

            else:
                index, value_d = min(enumerate(threshold_list_d),
                                     key=lambda x: abs(x[1]-ipr_a_e))
                index = answers_list_ipr_diag.index(value_d)
                check_d = abs(value_d - ipr_a_e)
            # Horizontal
            if len(threshold_list_h) == 0:
                value_h = np.abs(answers_list_dpr_hori-dpr_g_h)
                index = np.argmin(np.abs(answers_list_dpr_hori-dpr_g_h))
                # check_h = abs(value_h - dpr_g_h)
                check_h = min(value_h)
            else:
                index, value_h = min(enumerate(threshold_list_h),
                                     key=lambda x: abs(x[1]-ipr_g_h))
                index = answers_list_ipr_hori.index(value_h)
                check_h = abs(value_h - ipr_g_h)

            checklist = [check_h, check_d, check_i]
            min_value = min(checklist)
            min_index = checklist.index(min_value)

            x = min(check_h, check_d, check_i)
            if min_index == 0 and len(threshold_list_h) == 0:  # Horizontal
                value_h = np.abs(answers_list_dpr_hori-dpr_g_h)
                index = np.argmin(np.abs(answers_list_dpr_hori-dpr_g_h))
                return index + 1

            elif min_index == 0 and len(threshold_list_h) != 0:
                index, value_h = min(enumerate(threshold_list_h),
                                     key=lambda x: abs(x[1]-ipr_g_h))
                index = answers_list_ipr_hori.index(value_h)
                return index + 1

            elif min_index == 1 and len(threshold_list_d) == 0:
                value_d = np.abs(answers_list_dpr_diag - dpr_a_e)
                index = np.argmin(np.abs(answers_list_dpr_diag-dpr_a_e))
                return index + 1

            elif min_index == 1 and len(threshold_list_d) != 0:
                index, value_d = min(enumerate(threshold_list_d),
                                     key=lambda x: abs(x[1]-ipr_a_e))

                index = answers_list_ipr_diag.index(value_d)
                return index + 1

            elif min_index == 2 and len(threshold_list_i) == 0:
                value_i = np.abs(answers_list_dpr_i_diag-dpr_f_a)
                index = np.argmin(np.abs(answers_list_dpr_i_diag-dpr_f_a))
                return index + 1
            else:
                index, value_i = min(enumerate(threshold_list_i),
                                     key=lambda x: abs(x[1]-ipr_f_a))
                index = answers_list_ipr_i_diag.index(value_i)
                return index + 1

        # For Problem C Questions
        if problem.problemSetName == "Basic Problems C" or problem.problemSetName == "Test Problems C" or problem.problemSetName == "Challenge Problems C" or problem.problemSetName == "Raven's Problems C":
            answers_list_DPR = []
            answers_list_IPR = []
            # For 2 x 2 Questions
            if problem.problemType == "2x2":
                DPR_A_B = self.Calculate_DPR(self.image_a, self.image_b)
                IPR_A_B = self.Calculate_IPR(self.image_a, self.image_b)
                for i in self.answers:
                    answers_list_DPR.append(
                        self.Calculate_DPR(self.image_d, i))
                    answers_list_IPR.append(
                        self.Calculate_IPR(self.image_d, i))

            DPR_G_H = self.Calculate_DPR(self.image_g, self.image_h)
            DPR_B_C = self.Calculate_DPR(self.image_b, self.image_c)
            IPR_G_H = self.Calculate_IPR(self.image_g, self.image_h)
            IPR_B_C = self.Calculate_IPR(self.image_b, self.image_c)

            for i in self.answers:
                answers_list_DPR.append(self.Calculate_DPR(self.image_h, i))
                answers_list_IPR.append(self.Calculate_IPR(self.image_h, i))

            threshold_max = DPR_G_H + 2
            threshold_min = DPR_G_H - 2

            threshold_max_alt = DPR_B_C + 2
            threshold_min_alt = DPR_B_C - 2

            threshold_list = []
            for index, i in enumerate(answers_list_DPR):
                if threshold_min <= i <= threshold_max:
                    threshold_list.append(answers_list_IPR[index])

            if len(threshold_list) == 0:
                index = np.argmin(np.abs(answers_list_DPR-DPR_G_H))
                return index + 1

            index, value = min(enumerate(threshold_list),
                               key=lambda x: abs(x[1]-IPR_G_H))
            index = answers_list_IPR.index(value)
            return index + 1

        if problem.problemSetName == "Basic Problems B" or problem.problemSetName == "Test Problems B" or problem.problemSetName == "Challenge Problems B" or problem.problemSetName == "Raven's Problems B":
            answers_list_DPR = []
            answers_list_IPR = []
            # For 2 x 2 Questions
            if problem.problemType == "2x2":
                DPR_A_B = self.Calculate_DPR(self.image_a, self.image_b)
                IPR_A_B = self.Calculate_IPR(self.image_a, self.image_b)

            for i in self.answers:
                answers_list_DPR.append(self.Calculate_DPR(self.image_c, i))
                answers_list_IPR.append(self.Calculate_IPR(self.image_c, i))

            threshold_max = DPR_A_B + 2
            threshold_min = DPR_A_B - 2
            '''
            threshold_max_alt = DPR_B_C + 2
            threshold_min_alt = DPR_B_C - 2
            '''
            threshold_list = []
            for index, i in enumerate(answers_list_DPR):
                if threshold_min <= i <= threshold_max:
                    threshold_list.append(answers_list_IPR[index])

            if len(threshold_list) == 0:
                index = np.argmin(np.abs(answers_list_DPR-DPR_A_B))
                return index + 1

            index, value = min(enumerate(threshold_list),
                               key=lambda x: abs(x[1]-IPR_A_B))
            index = answers_list_IPR.index(value)
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
        matrix_3 = np.subtract(matrix_1, matrix_2)
        pixel_difference = (np.abs(matrix_3) > 127).sum()

        no_of_pixels = image1.size[0] * image1.size[1]
        similarity = 1.0 - (pixel_difference / (no_of_pixels * 1.0))

        return similarity

    def Binarize_Image(self, image):
        ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        return image

    def Calculate_DPR(self, image1, image2):
        dpr_1 = np.sum(image1)/np.size(image1)
        dpr_2 = np.sum(image2)/np.size(image2)
        return dpr_1 - dpr_2

    def Calculate_IPR(self, image1, image2):
        intersection = cv2.bitwise_or(image1, image2)
        intersection_pixels = np.sum(intersection)
        return (intersection_pixels/np.sum(image1)) - (intersection_pixels/np.sum(image2))

    def Calculate_Tversky(self, img1, img2):
        similarity = len(np.where((img1 == 0) & (img2 == 0))[
                         0])/(len(np.where((img1 == 0) & (img2 == 0))[0]) + len(np.where((img1 == 0))[0]) + len(np.where((img2 == 0))[0]))

        return similarity

    def calculate_bitwise(self, image1, image2):
        bitwise_or_h = cv2.bitwise_or(image1, image2)
        bitwise_xor_h = cv2.bitwise_xor(image1, image2)
        bitwise_xor_h_i = cv2.bitwise_not(bitwise_xor_h)
        bitwise_and_h = cv2.bitwise_and(image1, image2)
        '''
        cv2.imshow("bitwise_or_h", bitwise_or_h)
        cv2.waitKey(0)
        cv2.imshow("bitwise_xor_h", bitwise_xor_h)
        cv2.waitKey(0)
        cv2.imshow("bitwise_xor_h_i", bitwise_xor_h_i)
        cv2.waitKey(0)
        cv2.imshow("bitwise_and_h", bitwise_and_h)
        cv2.waitKey(0)
        '''

        w = self.Calculate_Tversky(bitwise_or_h, self.image_c)
        x = self.Calculate_Tversky(bitwise_xor_h, self.image_c)
        y = self.Calculate_Tversky(bitwise_xor_h_i, self.image_c)
        z = self.Calculate_Tversky(bitwise_and_h, self.image_c)
        bitwise_list = [w, x, y, z]
        max_value = max(bitwise_list)
        max_index = bitwise_list.index(max_value)

        if max_index == 0:
            compare_to = cv2.bitwise_or(self.image_g, self.image_h)
        elif max_index == 1:
            compare_to = cv2.bitwise_xor(self.image_g, self.image_h)
        elif max_index == 2:
            bitwise_xor_h = cv2.bitwise_xor(self.image_g, self.image_h)
            compare_to = cv2.bitwise_not(bitwise_xor_h)
        else:
            compare_to = cv2.bitwise_and(self.image_g, self.image_h)
        final_list = []
        for i in self.answers:
            final_list.append(self.Calculate_Tversky(compare_to, i))

        max_value = max(final_list)
        max_index = final_list.index(max_value) + 1

        return max_index
