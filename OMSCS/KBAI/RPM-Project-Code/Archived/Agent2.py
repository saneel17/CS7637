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
from PIL import Image, ImageChops, ImageOps
from random import randrange
import numpy
import os
import sys
import time
import math
import re

IMAGE_SIDE = 184
IMAGE_NONE_THRESHOLD = 99
IMAGE_TRANSPOSE_THRESHOLD = 97
APPLY_DIFFERENCE_THRESHOLD = 96
APPLY_DIFFERENCE_THRESHOLD_3x3 = 96
XOR_THRESHOLD = 95
OR_THRESHOLD = 97
AND_THRESHOLD = 95
XOR_THRESHOLD_3x3 = 94
SUBTRACT_THRESHOLD_3x3 = 95
OR_THRESHOLD_3x3 = 97
AND_THRESHOLD_3x3 = 95
DIAGONAL_THRESHOLD_3x3 = 95
SCORE_PIXEL_WEIGHT = 0.70
SCORE_RMS_WEIGHT = 1 - SCORE_PIXEL_WEIGHT
RGB_SUM = 30
ENV = 'prod'

DIFFERENCE_THRESHOLD = 1.5
SIMPLE_XOR_DIFFERENCE_THRESHOLD = 2.7
APPLY_DIFFERENCE_DIFFERENCE_THRESHOLD = 2.0


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        self.problem = None
        self.num_options = None
        self.is3x3 = False
        #self.time = time.clock()
        self.readyForSecondaryCompare = False
        self.toggleDirectionH = False
        self.toggleDirectionV = False
        self.toggleDirection = False
        self.isDirectionSetH = False
        self.isDirectionSetV = False
        # Current Directory
        self.cd = sys.path[0]

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self, problem):
        self.time = time.time()
        self.Initialize_Problem(problem)
        self.Problem_Heading_Printer()

        answer = None
        default_answer = -1
        transformations_list = [None, Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM, 'Rotate 45', Image.ROTATE_90, 'Rotate 135',
                                Image.ROTATE_180, 'Rotate 225', Image.ROTATE_270, 'Rotate 315', 'AND Images', 'OR Images',
                                'XOR Images', 'Apply Difference']
        transformations_done = []
        t_list_index = 0
        solution_found = False

        if self.is3x3:
            self.num_options = 8
            image_a, image_b, image_c, image_d, image_e, image_f, image_g, image_h = self.Load_Problem_Images()
            images = [image_a, image_b, image_c, image_d,
                      image_e, image_f, image_g, image_h]
            image_1, image_2, image_3, image_4, image_5, image_6, image_7, image_8 = self.Load_Problem_Answer_Images()
            answer_images = [image_1, image_2, image_3,
                             image_4, image_5, image_6, image_7, image_8]

            # AND_3x3_Answer, AND_3x3_Score = self.Get_AND_3x3_Answer(images)
            # OR_3x3_Answer, OR_3x3_Score = self.Get_OR_3x3_Answer(images)
            # XOR_3x3_Answer, XOR_3x3_Score = self.Get_XOR_3x3_Answer(images)
            # Subtract_3x3_Answer, Subtract_3x3_Score = self.Get_Subtract_3x3_Answer(images)
            # Apply_Difference_3x3_Answer, Apply_Difference_3x3_Score = self.Apply_Difference_3x3_Answer(images)
            AND_3x3_Answer_DPR, AND_3x3_Difference = self.Get_AND_3x3_Answer_DPR(
                images)
            OR_3x3_Answer_DPR, OR_3x3_Difference = self.Get_OR_3x3_Answer_DPR(
                images)
            # XOR_3x3_Answer_DPR, XOR_3x3_Difference = self.Get_XOR_3x3_Answer_DPR(images)
            # Simple_XOR_3x3_Answer_DPR, Simple_XOR_3x3_Difference = self.Get_Simple_XOR_3x3_Answer_DPR(images)
            Subtract_3x3_Answer_DPR, Subtract_3x3_Difference = self.Get_Subtract_3x3_Answer_DPR(
                images)
            # Apply_Difference_3x3_Answer, Apply_Difference_3x3_Difference = self.Apply_Difference_3x3_Answer_DPR(images)

            FigureCountPattern_Answer = self.Figure_Count_Pattern_3x3_Answer()
            Diagonal_Similarity_3x3_Answer_DPR, Diagonal_Similarity_3x3_Difference = self.Check_Diagonal_Similarity_3x3_DPR(
                images + answer_images)
            Diagonal_XOR_Similarity_3x3_Answer_DPR, Diagonal_XOR_Similarity_3x3_Difference = self.Check_Diagonal_XOR_Similarity_3x3_DPR(
                images + answer_images)

            answer_list = [AND_3x3_Answer_DPR, OR_3x3_Answer_DPR, Subtract_3x3_Answer_DPR,
                           Diagonal_Similarity_3x3_Answer_DPR, Diagonal_XOR_Similarity_3x3_Answer_DPR]
            # score_list = [AND_3x3_Score, OR_3x3_Score, XOR_3x3_Score, Subtract_3x3_Score]
            difference_list = [AND_3x3_Difference, OR_3x3_Difference, Subtract_3x3_Difference,
                               Diagonal_Similarity_3x3_Difference, Diagonal_XOR_Similarity_3x3_Difference]
            for d, index in zip(difference_list, range(len(difference_list))):
                if d == 0:
                    difference_list[index] = 100
            transformations = ['AND Images DPR', 'OR Images DPR', 'Subtract Images DPR',
                               'Diagonal Similarity DPR', 'Diagonal XOR Similarity DPR']

            # answer = answer_list[score_list.index(max(score_list))]
            print('Final DPR Results:', transformations,
                  answer_list, difference_list)
            answer = answer_list[difference_list.index(min(difference_list))]
            if answer != default_answer:
                # print('Solution found with `%s` . . . \n' % transformations[score_list.index(max(score_list))])
                print('Solution found with `%s` . . . \n' %
                      transformations[difference_list.index(min(difference_list))])
                if ENV == 'dev':
                    self.Print_Found_Match(answer)
            else:
                print('\nDPR Did not work, running IPR methods...')
                AND_3x3_Answer_IPR, AND_3x3_Score = self.Get_AND_3x3_Answer_IPR(
                    images)
                OR_3x3_Answer_IPR, OR_3x3_Score = self.Get_OR_3x3_Answer_IPR(
                    images)
                XOR_3x3_Answer_IPR, XOR_3x3_Score = self.Get_XOR_3x3_Answer_IPR(
                    images)
                Simple_XOR_3x3_Answer_IPR, Simple_XOR_3x3_Score = self.Get_Simple_XOR_3x3_Answer_IPR(
                    images)
                Subtract_3x3_Answer_IPR, Subtract_3x3_Score = self.Get_Subtract_3x3_Answer_IPR(
                    images)

                Diagonal_Similarity_3x3_Answer_IPR, Diagonal_Similarity_3x3_Score = self.Check_Diagonal_Similarity_3x3_IPR(
                    images + answer_images)
                Diagonal_XOR_Similarity_3x3_Answer_IPR, Diagonal_XOR_Similarity_3x3_Score = self.Check_Diagonal_XOR_Similarity_3x3_IPR(
                    images + answer_images)

                answer_list = [AND_3x3_Answer_IPR, OR_3x3_Answer_IPR, XOR_3x3_Answer_IPR, Simple_XOR_3x3_Answer_IPR,
                               Subtract_3x3_Answer_IPR, Diagonal_Similarity_3x3_Answer_IPR, Diagonal_XOR_Similarity_3x3_Answer_IPR]
                score_list = [AND_3x3_Score, OR_3x3_Score, XOR_3x3_Score, Simple_XOR_3x3_Score,
                              Subtract_3x3_Score, Diagonal_Similarity_3x3_Score, Diagonal_XOR_Similarity_3x3_Score]

                transformations = ['AND Images IPR', 'OR Images IPR', 'XOR Images IPR', 'Simple XOR Images IPR',
                                   'Subtract Images IPR', 'Diagonal Similarity IPR', 'Diagonal XOR Similarity IPR']
                print('Final IPR Results:', transformations,
                      answer_list, score_list)
                answer = answer_list[score_list.index(max(score_list))]
                if answer != default_answer:
                    print('Solution found with `%s` . . . \n' %
                          transformations[score_list.index(max(score_list))])
                    if ENV == 'dev':
                        self.Print_Found_Match(answer)
            # elif FigureCountPattern_Answer != 1:
            #     answer = FigureCountPattern_Answer
            #     if ENV == 'dev' and answer != default_answer:
            #         self.Print_Found_Match(answer)

            # if Apply_Difference_3x3_Answer != default_answer and answer == default_answer:
            #     answer = Apply_Difference_3x3_Answer
            #     if ENV == 'dev' and answer != default_answer:
            #         self.Print_Found_Match(answer)
        else:
            self.num_options = 6
            image_a, image_b, image_c = self.Load_Problem_Images()

            while solution_found == False and t_list_index < len(transformations_list):
                transformation_string = self.Transformation_Dict(
                )[str(transformations_list[t_list_index])]
                print('SOLVING with `%s` Transformation . . . \n' %
                      transformation_string)
                transformations_done.append(transformation_string)
                threshold = self.Threshold_Dict()[transformation_string]

                if 'Difference' in transformation_string:
                    find_difference_AB = self.XOR_images(image_a, image_b)
                    find_difference_AC = self.XOR_images(image_a, image_c)
                    image_b_added_diff = self.OR_images(
                        image_b, find_difference_AC)
                    image_c_added_diff = self.OR_images(
                        image_c, find_difference_AB)
                    image_b_removed_diff = self.AND_images(
                        image_b, find_difference_AC)
                    image_c_removed_diff = self.AND_images(
                        image_c, find_difference_AB)
                    print('Adding Difference')
                    print(
                        'Looking for a match for C*(A-B) to D or B*(A-C) to D . . . \n')
                    for i in range(1, self.num_options+1):
                        print('Testing Answer %d . . . ' % i)
                        image_d = self.Load_Image(str(i))
                        score_diff_h = self.PixelCompare(
                            image_c_added_diff, image_d, transformations_list[t_list_index], transformations_done)
                        score_diff_v = self.PixelCompare(
                            image_b_added_diff, image_d, transformations_list[t_list_index], transformations_done)
                        if score_diff_h > score_diff_v:
                            print('C*(A-B) to D is a better match with a score of %f > %f' %
                                  (score_diff_h, score_diff_v))
                            if score_diff_h > threshold:
                                answer = i
                                solution_found = True
                                self.Print_Found_Match(answer)
                            else:
                                print('%f is lower than the the threshold %f . . . ' % (
                                    score_diff_h, threshold))
                        else:
                            print('B*(A-C) to D is a better match with a score of %f > %f' %
                                  (score_diff_v, score_diff_h))
                            if score_diff_v > threshold:
                                answer = i
                                solution_found = True
                                self.Print_Found_Match(answer)
                            else:
                                print('%f is lower than the the threshold %f . . . ' % (
                                    score_diff_h, threshold))
                    if solution_found:
                        break
                    else:
                        answer = default_answer
                    print('Removing Difference')
                    print(
                        'Looking for a match for C+(A-B) to D or B+(A-C) to D . . . \n')
                    for i in range(1, self.num_options+1):
                        print('Testing Answer %d . . . ' % i)
                        image_d = self.Load_Image(str(i))
                        score_diff_h = self.PixelCompare(
                            image_c_removed_diff, image_d, transformations_list[t_list_index], transformations_done)
                        score_diff_v = self.PixelCompare(
                            image_b_removed_diff, image_d, transformations_list[t_list_index], transformations_done)
                        if score_diff_h > score_diff_v:
                            print('C+(A-B) to D is a better match with a score of %f > %f' %
                                  (score_diff_h, score_diff_v))
                            if score_diff_h > threshold:
                                answer = i
                                solution_found = True
                                self.Print_Found_Match(answer)
                            else:
                                print('%f is lower than the the threshold %f . . . ' % (
                                    score_diff_h, threshold))
                        else:
                            print('B+(A-C) to D is a better match with a score of %f > %f' %
                                  (score_diff_v, score_diff_h))
                            if score_diff_v > threshold:
                                answer = i
                                solution_found = True
                                self.Print_Found_Match(answer)
                            else:
                                print('%f is lower than the the threshold %f . . . ' % (
                                    score_diff_h, threshold))
                    break
                print(
                    'Checking which relationship is stronger: A to B or A to C . . . \n')
                print('-- A to B --')
                if transformation_string == 'None' and self.Duplicate_Check(image_a, image_b):
                    print('Duplicate!')
                    print('-- C to D --')
                    for i in range(1, self.num_options+1):
                        print('Testing Answer %d . . . ' % i)
                        image_d = self.Load_Image(str(i))
                        if self.Duplicate_Check(image_c, image_d):
                            answer = i
                            solution_found = True
                            self.Print_Found_Match(answer)
                A_to_B_score = self.PixelCompare(
                    image_a, image_b, transformations_list[t_list_index], transformations_done)
                if self.toggleDirection:
                    self.toggleDirectionH = True
                    self.toggleDirection = False
                self.isDirectionSetH = True
                print('-- A to C --')
                if transformation_string == 'None' and self.Duplicate_Check(image_a, image_c):
                    print('Duplicate!')
                    print('-- B to D --')
                    for i in range(1, self.num_options+1):
                        print('Testing Answer %d . . . ' % i)
                        image_d = self.Load_Image(str(i))
                        if self.Duplicate_Check(image_b, image_d):
                            answer = i
                            solution_found = True
                            self.Print_Found_Match(answer)
                A_to_C_score = self.PixelCompare(
                    image_a, image_c, transformations_list[t_list_index], transformations_done)
                if self.toggleDirection:
                    self.toggleDirectionV = True
                    self.toggleDirection = False
                self.isDirectionSetV = True

                print()
                print('No duplicates . . . ')
                self.readyForSecondaryCompare = True

                if A_to_B_score >= A_to_C_score:
                    print('-- A to B is stronger or the same --')
                    if A_to_B_score >= threshold:
                        print('-- C to D --')
                        max_score = 0
                        for i in range(1, self.num_options+1):
                            print('Testing Answer %d . . . ' % i)
                            image_d = self.Load_Image(str(i))
                            C_to_D_score = self.PixelCompare(
                                image_c, image_d, transformations_list[t_list_index], transformations_done)
                            if C_to_D_score >= threshold and max_score < C_to_D_score:
                                max_score = C_to_D_score
                                answer = i
                                solution_found = True
                            elif C_to_D_score >= threshold and max_score == C_to_D_score:
                                answer = default_answer
                                solution_found = False
                                break
                    else:
                        print('%f is lower than the the threshold %f . . . ' %
                              (A_to_B_score, threshold))
                else:
                    print('-- A to C is stronger --')
                    if A_to_C_score >= threshold:
                        print('-- B to D --')
                        self.isDirectionSetH = False
                        max_score = 0
                        for i in range(1, self.num_options+1):
                            print('Testing Answer %d . . . ' % i)
                            image_d = self.Load_Image(str(i))
                            B_to_D_score = self.PixelCompare(
                                image_b, image_d, transformations_list[t_list_index], transformations_done)
                            if B_to_D_score >= threshold and max_score < B_to_D_score:
                                max_score = B_to_D_score
                                answer = i
                                solution_found = True
                            elif B_to_D_score >= threshold and max_score == B_to_D_score:
                                answer = default_answer
                                solution_found = False
                    else:
                        print('%f is lower than the the threshold %f . . . ' %
                              (A_to_C_score, threshold))
                self.readyForSecondaryCompare = False
                self.isDirectionSetV = False
                self.isDirectionSetH = False
                self.toggleDirectionV = False
                self.toggleDirectionH = False
                if solution_found:
                    self.Print_Found_Match(answer)
                else:
                    self.Print_No_Match()
                print()
                t_list_index += 1
        self.Print_Time_Elapsed()

        if answer is None or answer == default_answer:
            if ENV != 'dev':
                answer = self.Get_Guess()
        return answer

    def Get_Guess(self):
        guess = randrange(1, self.num_options)
        if ENV == 'dev':
            print('???????????????????????????????????????????????????')
            print('                ~`* GUESSING %d*`~' % guess)
            print('???????????????????????????????????????????????????')
        return guess

    def Apply_Difference_3x3_Answer_DPR(self, images):
        im_a, im_b, im_c, im_d, im_e, im_f, im_g, im_h = images
        transformation = 'Apply Difference'
        if ENV == 'dev':
            print('SOLVING with `%s` Transformation . . . \n' % transformation)

        # OR_FH_Answer = self.OR_images(im_f, im_h)
        dual_pattern_image = self.OR_images(
            self.AND_images(im_g, im_h), self.AND_images(im_c, im_f))

        results = []
        for i in range(1, self.num_options+1):
            im_i = self.Load_Image(str(i))
            # score = self.PixelCompare_3x3(OR_FH_Answer, im_i, transformation)
            difference = self.Similarity_Check(dual_pattern_image, im_i)
            # results.append(score)
            results.append((i, abs(difference)))
        # print('Apply Difference Scores:', scores)
        print('Apply Difference Results:', results)
        if ENV == 'dev':
            input()
        # if max(results) > APPLY_DIFFERENCE_THRESHOLD_3x3:
        if sorted(results, key=lambda x: x[1])[0][1] < APPLY_DIFFERENCE_DIFFERENCE_THRESHOLD:
            return sorted(results, key=lambda x: x[1])[0]
        return -1, 0

    def Apply_Difference_3x3_Answer_IPR(self, images):
        im_a, im_b, im_c, im_d, im_e, im_f, im_g, im_h = images
        transformation = 'Apply Difference'
        if ENV == 'dev':
            print('SOLVING with `%s` Transformation . . . \n' % transformation)

        dual_pattern_image = self.OR_images(
            self.AND_images(im_g, im_h), self.AND_images(im_c, im_f))

        results = []
        for i in range(1, self.num_options+1):
            im_i = self.Load_Image(str(i))
            score = self.PixelCompare_3x3(
                dual_pattern_image, im_i, transformation)
            # difference = self.Similarity_Check(dual_pattern_image, im_i)
            results.append((i, score))
            # results.append((i, abs(difference)))
        print('Apply Difference Scores:', results)
        # print('Apply Difference Results:', results)
        if ENV == 'dev':
            input()
        # if max(results) > APPLY_DIFFERENCE_THRESHOLD_3x3:
        if sorted(results, key=lambda x: x[1])[0][1] > APPLY_DIFFERENCE_THRESHOLD_3x3:
            return sorted(results, key=lambda x: x[1])[0]
        return -1, 0

    def Check_Diagonal_Similarity_3x3_DPR(self, images):
        a, b, c, d, e, f, g, h, i1, i2, i3, i4, i5, i6, i7, i8 = images
        answers = [i1, i2, i3, i4, i5, i6, i7, i8]

        transformation = 'Diagonal Similarity DPR'
        if ENV == 'dev':
            print('SOLVING with `%s` Transformation . . . \n' % transformation)

        # Checking for Diagonal Pattern 1
        # [A] (B) {C}
        # {D} [E] (F)
        # (G) {H} [I]
        print('Checking Pattern 1 . . .\n')
        # print('Step 1: Filter out differences with AND . . .\n')
        # # (Group 1)
        # bf = self.AND_images(b, f)
        # fg = self.AND_images(f, g)
        # bg = self.AND_images(b, g)
        # # {Group 2}
        # cd = self.AND_images(c, d)
        # dh = self.AND_images(d, h)
        # ch = self.AND_images(c, h)
        # # [Group 3]
        # ae = self.AND_images(a, e)
        # print('Checking similarities with AND . . .\n')
        # score_G1 = self.Similarity_Check_3x3(bf, fg, bg)
        # score_G2 = self.Similarity_Check_3x3(cd, dh, ch)
        # print('Score Group 1:', score_G1)
        # print('Score Group 2:', score_G2)
        difference_G1 = self.Similarity_Check_3x3_DPR(b, f, g)
        difference_G2 = self.Similarity_Check_3x3_DPR(c, d, h)
        print('Difference Group 1:', difference_G1)
        print('Difference Group 2:', difference_G2)
        # if score_G1 > DIAGONAL_THRESHOLD_3x3 and score_G2 > DIAGONAL_THRESHOLD_3x3:
        if abs(difference_G1) < DIFFERENCE_THRESHOLD and abs(difference_G2) < DIFFERENCE_THRESHOLD:
            filtered_results = []
            if self.Similarity_Check_DPR(a, e) == 0 or abs(self.Similarity_Check_DPR(a, e)) < 0.001:
                print('\nImage E is too close in size to Image A...')
                filtered_results = zip(answers, range(1, len(answers)+1))
            elif self.Similarity_Check_DPR(a, e) < 0:
                print(
                    '\nImage E is smaller than Image A so Image I must be smaller than Image E...')
                for i, answer in zip(answers, range(1, len(answers)+1)):
                    if self.Similarity_Check_DPR(e, i) < 0:
                        filtered_results.append((i, answer))
            else:
                print(
                    '\nImage E is bigger than Image A so Image I must be bigger than Image E...')
                for i, answer in zip(answers, range(1, len(answers)+1)):
                    if self.Similarity_Check_DPR(e, i) >= 0:
                        filtered_results.append((i, answer))
            print('\nFiltered Results:', filtered_results)
            results = []
            for i, answer in filtered_results:
                # [Group 3] continued
                ei = self.AND_images(e, i)
                ai = self.AND_images(a, i)
                # score_G3 = self.Similarity_Check_3x3(ai, ei, ae)
                difference_G3 = self.Similarity_Check_3x3_DPR(a, e, i)
                # score_G3 > DIAGONAL_THRESHOLD_3x3:
                if abs(difference_G3) < DIFFERENCE_THRESHOLD:
                    # results.append((score_G3, answer))
                    results.append((answer, abs(difference_G3)))
                    # if ENV == 'dev':
                    #     print('+ [%d] Score %f > %f' % (answer, score_G3, DIAGONAL_THRESHOLD_3x3))
                # else:
                #     if ENV == 'dev':
                #         print('- [%d] Score %f < %f' % (answer, score_G3, DIAGONAL_THRESHOLD_3x3))
            if ENV == 'dev':
                print('Results:', results)
            if results != []:
                if len(results) > 1 and len(results) < 8:
                    # More than one diagonal pattern detected
                    # (A*E) - (B*D) accounts for both diagonal patterns of I
                    #
                    #   $[A] %(B) *{C}
                    #   %{D} *[E] $(F)
                    #   *(G) ${H} %[I]
                    #
                    # Pattern 1 Second Pattern Groups - *, %, @
                    print(
                        '\nMore than one diagonal pattern detected, running tiebreaker comparison . . . ')
                    # dual_pattern_image = self.OR_images(self.AND_images(a, e), self.AND_images(b, d))
                    dual_pattern_image = self.OR_images(
                        self.OR_images(a, e), self.OR_images(b, d))
                    tiebreaker_results = []
                    for ans, sc in results:
                        tiebreaker_results.append((ans, abs(self.Similarity_Check_DPR(
                            dual_pattern_image, self.Load_Image(str(ans))))))
                    print(tiebreaker_results)
                    # best_answer = max(tiebreaker_results)[1]
                    best_result = sorted(
                        tiebreaker_results, key=lambda x: x[1])[0]
                elif len(results) == 8:
                    print('\nToo many matched results, skipping...')
                    return -1, 0
                else:
                    best_result = results[0]
                print('\nResult with highest similarity:', best_result)
                return best_result
        # Checking for Diagonal Pattern 2
        # {A} (B) [C]
        # (D) [E] {F}
        # [G] {H} (I)
        print('Checking Pattern 2 . . .\n')
        print('Step 1: Filter out differences with AND . . .\n')
        # (Group 1)
        bd = self.AND_images(b, d)
        # {Group 2}
        af = self.AND_images(a, f)
        fh = self.AND_images(f, h)
        ah = self.AND_images(a, h)
        # [Group 3]
        ce = self.AND_images(c, e)
        eg = self.AND_images(e, g)
        cg = self.AND_images(c, g)
        print('Step 2: Checking similarities with AND . . .\n')
        # score_G2 = self.Similarity_Check_3x3(af, fh, ah)
        # score_G3 = self.Similarity_Check_3x3(ce, eg, cg)
        # print('Score Group 2:', score_G2)
        # print('Score Group 3:', score_G3)
        difference_G2 = self.Similarity_Check_3x3_DPR(a, f, h)
        difference_G3 = self.Similarity_Check_3x3_DPR(c, e, g)
        print('Difference Group 2:', difference_G2)
        print('Difference Group 3:', difference_G3)
        # if score_G3 > DIAGONAL_THRESHOLD_3x3 and score_G2 > DIAGONAL_THRESHOLD_3x3:
        if abs(difference_G3) < DIFFERENCE_THRESHOLD and abs(difference_G2) < DIFFERENCE_THRESHOLD:
            filtered_results = []
            if self.Similarity_Check_DPR(b, d) == 0 or abs(self.Similarity_Check_DPR(b, d)) < 0.001:
                print('\nImage D is too close in size to Image B...')
                filtered_results = zip(answers, range(1, len(answers)+1))
            elif self.Similarity_Check_DPR(b, d) < 0:
                print(
                    '\nImage D is smaller than Image B so Image I must be smaller than Image D...')
                for i, answer in zip(answers, range(1, len(answers)+1)):
                    if self.Similarity_Check_DPR(d, i) < 0:
                        filtered_results.append((i, answer))
            else:
                print(
                    '\nImage D is bigger than Image B so Image I must be bigger than Image D...')
                for i, answer in zip(answers, range(1, len(answers)+1)):
                    if self.Similarity_Check_DPR(d, i) >= 0:
                        filtered_results.append((i, answer))
            print('\nFiltered Results:', filtered_results)
            results = []
            for i, answer in filtered_results:
                # [Group] continued
                di = self.AND_images(d, i)
                bi = self.AND_images(b, i)
                # score_G1 = self.Similarity_Check_3x3(bi, di, bd)
                difference_G1 = self.Similarity_Check_3x3_DPR(b, d, i)

                # score_G1 > DIAGONAL_THRESHOLD_3x3:
                if abs(difference_G1) < DIFFERENCE_THRESHOLD:
                    # results.append((score_G1, answer))
                    results.append((answer, abs(difference_G3)))
                #     if ENV == 'dev':
                #         print('+ [%d] Score %f > %f' % (answer, score_G1, DIAGONAL_THRESHOLD_3x3))
                # else:
                #     if ENV == 'dev':
                #         print('- [%d] Score %f < %f' % (answer, score_G1, DIAGONAL_THRESHOLD_3x3))
            print(results)
            if results != []:
                if ENV == 'dev':
                    print(results)
                if len(results) > 1 and len(results) < 8:
                    # More than one diagonal pattern detected
                    # (A*E) - (B*D) accounts for both diagonal patterns of I
                    #
                    #   * {A}  @ (B)  % [C]
                    #   % (D)  * [E]  @ {F}
                    #   @ [G]  % {H}  * (I)
                    #
                    # Pattern 2 Second Pattern Groups - *, %, @
                    print(
                        '\nMore than one diagonal pattern detected, running tiebreaker comparison . . . ')
                    # dual_pattern_image = self.OR_images(self.AND_images(a, e), self.AND_images(b, d))
                    dual_pattern_image = self.OR_images(
                        self.OR_images(a, e), self.OR_images(b, d))
                    tiebreaker_results = []
                    for ans, sc in results:
                        tiebreaker_results.append((ans, abs(self.Similarity_Check_DPR(
                            dual_pattern_image, self.Load_Image(str(ans))))))
                    print(tiebreaker_results)
                    # best_answer = max(tiebreaker_results)[1]
                    best_result = sorted(
                        tiebreaker_results, key=lambda x: x[1])[0]
                elif len(results) == 8:
                    print('\nToo many matched results, skipping...')
                    return -1, 0
                else:
                    best_result = results[0]
                if ENV == 'dev':
                    print('\nResult with highest similarity:', best_result)
                return best_result
        return -1, 0

    def Check_Diagonal_Similarity_3x3_IPR(self, images):
        a, b, c, d, e, f, g, h, i1, i2, i3, i4, i5, i6, i7, i8 = images
        answers = [i1, i2, i3, i4, i5, i6, i7, i8]

        transformation = 'Diagonal Similarity IPR'
        if ENV == 'dev':
            print('SOLVING with `%s` Transformation . . . \n' % transformation)

        # Checking for Diagonal Pattern 1
        # [A] (B) {C}
        # {D} [E] (F)
        # (G) {H} [I]
        print('Checking Pattern 1 . . .\n')
        print('Step 1: Filter out differences with AND . . .\n')
        # (Group 1)
        bf = self.AND_images(b, f)
        fg = self.AND_images(f, g)
        bg = self.AND_images(b, g)
        # {Group 2}
        cd = self.AND_images(c, d)
        dh = self.AND_images(d, h)
        ch = self.AND_images(c, h)
        # [Group 3]
        ae = self.AND_images(a, e)
        print('Step 2: Checking similarities with AND . . .\n')
        score_G1 = self.Similarity_Check_3x3_IPR(bf, fg, bg)
        score_G2 = self.Similarity_Check_3x3_IPR(cd, dh, ch)
        print('Score Group 1:', score_G1)
        print('Score Group 2:', score_G2)
        if score_G1 > DIAGONAL_THRESHOLD_3x3 and score_G2 > DIAGONAL_THRESHOLD_3x3:
            results = []
            for i, answer in zip(answers, range(1, len(answers)+1)):
                # [Group 3] continued
                ei = self.AND_images(e, i)
                ai = self.AND_images(a, i)
                score_G3 = self.Similarity_Check_3x3_IPR(ai, ei, ae)
                if score_G3 > DIAGONAL_THRESHOLD_3x3:
                    results.append((answer, score_G3))
                    if ENV == 'dev':
                        print('+ [%d] Score %f > %f' %
                              (answer, score_G3, DIAGONAL_THRESHOLD_3x3))
                else:
                    if ENV == 'dev':
                        print('- [%d] Score %f < %f' %
                              (answer, score_G3, DIAGONAL_THRESHOLD_3x3))
            if ENV == 'dev':
                print('Results:', results)
            if results != []:
                if len(results) > 1 and len(results) < 8:
                    # More than one diagonal pattern detected
                    # (A*E) - (B*D) accounts for both diagonal patterns of I
                    #
                    #   $[A] %(B) *{C}
                    #   %{D} *[E] $(F)
                    #   *(G) ${H} %[I]
                    #
                    # Pattern 1 Second Pattern Groups - *, %, @
                    print(
                        '\nMore than one diagonal pattern detected, running tiebreaker comparison . . . ')
                    dual_pattern_image = self.OR_images(
                        self.AND_images(a, e), self.AND_images(b, d))
                    # dual_pattern_image = self.OR_images(self.OR_images(a, e), self.OR_images(b, d))
                    tiebreaker_results = []
                    for ans, sc in results:
                        tiebreaker_results.append((ans, self.Similarity_Check_IPR(
                            dual_pattern_image, self.Load_Image(str(ans)))))
                    print(tiebreaker_results)
                    # best_answer = max(tiebreaker_results)[1]
                    best_result = sorted(
                        tiebreaker_results, key=lambda x: x[1])[-1]
                elif len(results) == 8:
                    print('\nToo many matched results, skipping...')
                    return -1, 0
                else:
                    best_result = results[0]
                print('\nResult with highest similarity:', best_result)
                return best_result
        # Checking for Diagonal Pattern 2
        # {A} (B) [C]
        # (D) [E] {F}
        # [G] {H} (I)
        print('Checking Pattern 2 . . .\n')
        print('Step 1: Filter out differences with AND . . .\n')
        # (Group 1)
        bd = self.AND_images(b, d)
        # {Group 2}
        af = self.AND_images(a, f)
        fh = self.AND_images(f, h)
        ah = self.AND_images(a, h)
        # [Group 3]
        ce = self.AND_images(c, e)
        eg = self.AND_images(e, g)
        cg = self.AND_images(c, g)
        print('Step 2: Checking similarities with AND . . .\n')
        score_G2 = self.Similarity_Check_3x3_IPR(af, fh, ah)
        score_G3 = self.Similarity_Check_3x3_IPR(ce, eg, cg)
        print('Score Group 2:', score_G2)
        print('Score Group 3:', score_G3)
        if score_G3 > DIAGONAL_THRESHOLD_3x3 and score_G2 > DIAGONAL_THRESHOLD_3x3:
            results = []
            for i, answer in zip(answers, range(1, len(answers)+1)):
                # [Group] continued
                di = self.AND_images(d, i)
                bi = self.AND_images(b, i)
                score_G1 = self.Similarity_Check_3x3_IPR(bi, di, bd)

                if score_G1 > DIAGONAL_THRESHOLD_3x3:
                    results.append((answer, score_G1))
                    if ENV == 'dev':
                        print('+ [%d] Score %f > %f' %
                              (answer, score_G1, DIAGONAL_THRESHOLD_3x3))
                else:
                    if ENV == 'dev':
                        print('- [%d] Score %f < %f' %
                              (answer, score_G1, DIAGONAL_THRESHOLD_3x3))
            print(results)
            if results != []:
                if ENV == 'dev':
                    print(results)
                if len(results) > 1 and len(results) < 8:
                    # More than one diagonal pattern detected
                    # (A*E) - (B*D) accounts for both diagonal patterns of I
                    #
                    #   * {A}  @ (B)  % [C]
                    #   % (D)  * [E]  @ {F}
                    #   @ [G]  % {H}  * (I)
                    #
                    # Pattern 2 Second Pattern Groups - *, %, @
                    print(
                        '\nMore than one diagonal pattern detected, running tiebreaker comparison . . . ')
                    dual_pattern_image = self.OR_images(
                        self.AND_images(a, e), self.AND_images(b, d))
                    # dual_pattern_image = self.OR_images(self.OR_images(a, e), self.OR_images(b, d))
                    tiebreaker_results = []
                    for ans, sc in results:
                        tiebreaker_results.append((ans, abs(self.Similarity_Check_IPR(
                            dual_pattern_image, self.Load_Image(str(ans))))))
                    print(tiebreaker_results)
                    # best_answer = max(tiebreaker_results)[1]
                    best_result = sorted(
                        tiebreaker_results, key=lambda x: x[1])[-1]
                elif len(results) == 8:
                    print('\nToo many matched results, skipping...')
                    return -1, 0
                else:
                    best_result = results[0]
                if ENV == 'dev':
                    print('\nResult with highest similarity:', best_result)
                return best_result
        return -1, 0

    def Check_Diagonal_XOR_Similarity_3x3_DPR(self, images):
        a, b, c, d, e, f, g, h, i1, i2, i3, i4, i5, i6, i7, i8 = images
        answers = [i1, i2, i3, i4, i5, i6, i7, i8]

        transformation = 'Diagonal XOR Similarity DPR'
        if ENV == 'dev':
            print('SOLVING with `%s` Transformation . . . \n' % transformation)

        # Checking for Diagonal Pattern 1
        # [A] (B) {C}
        # {D} [E] (F)
        # (G) {H} [I]
        print('Checking Pattern 1 . . .\n')
        print('Step 1: Filter out differences with AND . . .\n')
        # (Group 1)
        bf = self.XOR_images(b, f)
        fg = self.XOR_images(f, g)
        bg = self.XOR_images(b, g)
        # {Group 2}
        cd = self.XOR_images(c, d)
        dh = self.XOR_images(d, h)
        ch = self.XOR_images(c, h)
        # [Group 3]
        ae = self.XOR_images(a, e)
        print('Step 2: Checking similarities with AND . . .\n')
        # score_G1 = self.Similarity_Check_3x3(bf, fg, bg)
        # score_G2 = self.Similarity_Check_3x3(cd, dh, ch)
        # print('Score Group 1:', score_G1)
        # print('Score Group 2:', score_G2)
        difference_G1 = self.Similarity_Check_3x3_DPR(bf, fg, bg)
        difference_G2 = self.Similarity_Check_3x3_DPR(cd, dh, ch)
        print('Difference Group 1:', difference_G1)
        print('Difference Group 2:', difference_G2)
        if abs(difference_G1) == 0 or abs(difference_G2) == 0:
            print(
                '\nThree of the shapes are exactly the same, this is not the right heuristic...')
            return -1, 0
        # if score_G1 > DIAGONAL_THRESHOLD_3x3 and score_G2 > DIAGONAL_THRESHOLD_3x3:
        if abs(difference_G1) < DIFFERENCE_THRESHOLD and abs(difference_G2) < DIFFERENCE_THRESHOLD:
            filtered_results = []
            if self.Similarity_Check_DPR(self.XOR_images(a, e), e) == 0 or abs(self.Similarity_Check_DPR(a, e)) < 0.001:
                print('\nImage E is too close in size to Image A...')
                filtered_results = zip(answers, range(1, len(answers)+1))
            elif self.Similarity_Check_DPR(self.XOR_images(a, e), e) < 0:
                print(
                    '\nImage E is smaller than Image A so Image I must be smaller than Image E...')
                for i, answer in zip(answers, range(1, len(answers)+1)):
                    if self.Similarity_Check_DPR(self.XOR_images(e, i), i) < 0:
                        filtered_results.append((i, answer))
            else:
                print(
                    '\nImage E is bigger than Image A so Image I must be bigger than Image E...')
                for i, answer in zip(answers, range(1, len(answers)+1)):
                    if self.Similarity_Check_DPR(self.XOR_images(e, i), i) >= 0:
                        filtered_results.append((i, answer))
            print('\nFiltered Results:', filtered_results)
            results = []
            for i, answer in filtered_results:
                # [Group 3] continued
                ei = self.XOR_images(e, i)
                ai = self.XOR_images(a, i)
                # score_G3 = self.Similarity_Check_3x3(ai, ei, ae)
                difference_G3 = self.Similarity_Check_3x3_DPR(ai, ei, ae)
                # score_G3 > DIAGONAL_THRESHOLD_3x3:
                if abs(difference_G3) < DIFFERENCE_THRESHOLD:
                    # results.append((score_G3, answer))
                    results.append((answer, abs(difference_G3)))
                    # if ENV == 'dev':
                    #     print('+ [%d] Score %f > %f' % (answer, score_G3, DIAGONAL_THRESHOLD_3x3))
                # else:
                #     if ENV == 'dev':
                #         print('- [%d] Score %f < %f' % (answer, score_G3, DIAGONAL_THRESHOLD_3x3))
            if ENV == 'dev':
                print('Results:', results)
            if results != []:
                if len(results) > 1 and len(results) < 8:
                    # More than one diagonal pattern detected
                    # (A*E) - (B*D) accounts for both diagonal patterns of I
                    #
                    #   $[A] %(B) *{C}
                    #   %{D} *[E] $(F)
                    #   *(G) ${H} %[I]
                    #
                    # Pattern 1 Second Pattern Groups - *, %, @
                    print(
                        '\nMore than one diagonal pattern detected, running tiebreaker comparison . . . ')
                    # dual_pattern_image = self.OR_images(self.AND_images(a, e), self.AND_images(b, d))
                    dual_pattern_image = self.OR_images(
                        self.OR_images(a, e), self.OR_images(b, d))
                    tiebreaker_results = []
                    for ans, sc in results:
                        tiebreaker_results.append((ans, abs(self.Similarity_Check_DPR(
                            dual_pattern_image, self.Load_Image(str(ans))))))
                    print(tiebreaker_results)
                    # best_answer = max(tiebreaker_results)[1]
                    best_result = sorted(
                        tiebreaker_results, key=lambda x: x[1])[0]
                elif len(results) == 8:
                    print('\nToo many matched results, skipping...')
                    return -1, 0
                else:
                    best_result = results[0]
                print('\nResult with highest similarity:', best_result)
                return best_result
        # Checking for Diagonal Pattern 2
        # {A} (B) [C]
        # (D) [E] {F}
        # [G] {H} (I)
        print('Checking Pattern 2 . . .\n')
        print('Step 1: Filter out differences with AND . . .\n')
        # (Group 1)
        bd = self.XOR_images(b, d)
        # {Group 2}
        af = self.XOR_images(a, f)
        fh = self.XOR_images(f, h)
        ah = self.XOR_images(a, h)
        # [Group 3]
        ce = self.XOR_images(c, e)
        eg = self.XOR_images(e, g)
        cg = self.XOR_images(c, g)
        print('Step 2: Checking similarities with AND . . .\n')
        # score_G2 = self.Similarity_Check_3x3(af, fh, ah)
        # score_G3 = self.Similarity_Check_3x3(ce, eg, cg)
        # print('Score Group 2:', score_G2)
        # print('Score Group 3:', score_G3)
        difference_G2 = self.Similarity_Check_3x3_DPR(af, fh, ah)
        difference_G3 = self.Similarity_Check_3x3_DPR(ce, eg, cg)
        print('Difference Group 2:', difference_G2)
        print('Difference Group 3:', difference_G3)
        if abs(difference_G2) == 0 or abs(difference_G3) == 0:
            print(
                '\nThree of the shapes are exactly the same, this is not the right heuristic...')
            return -1, 0
        # if score_G3 > DIAGONAL_THRESHOLD_3x3 and score_G2 > DIAGONAL_THRESHOLD_3x3:
        if abs(difference_G3) < DIFFERENCE_THRESHOLD and abs(difference_G2) < DIFFERENCE_THRESHOLD:
            filtered_results = []
            if self.Similarity_Check_DPR(self.XOR_images(b, d), d) == 0 or abs(self.Similarity_Check_DPR(self.XOR_images(b, d), d)) < 0.001:
                print('\nImage D is too close in size to Image B...')
                filtered_results = zip(answers, range(1, len(answers)+1))
            elif self.Similarity_Check_DPR(self.XOR_images(b, d), d) < 0:
                print(
                    '\nImage D is smaller than Image B so Image I must be smaller than Image D...')
                for i, answer in zip(answers, range(1, len(answers)+1)):
                    if self.Similarity_Check_DPR(self.XOR_images(d, i), i) < 0:
                        filtered_results.append((i, answer))
            else:
                print(
                    '\nImage D is bigger than Image B so Image I must be bigger than Image D...')
                for i, answer in zip(answers, range(1, len(answers)+1)):
                    if self.Similarity_Check_DPR(self.XOR_images(d, i), i) >= 0:
                        filtered_results.append((i, answer))
            print('\nFiltered Results:', filtered_results)
            results = []
            for i, answer in filtered_results:
                # [Group] continued
                di = self.XOR_images(d, i)
                bi = self.XOR_images(b, i)
                # score_G1 = self.Similarity_Check_3x3(bi, di, bd)
                difference_G1 = self.Similarity_Check_3x3_DPR(bi, di, bd)

                # score_G1 > DIAGONAL_THRESHOLD_3x3:
                if abs(difference_G1) < DIFFERENCE_THRESHOLD:
                    # results.append((score_G1, answer))
                    results.append((answer, abs(difference_G3)))
                #     if ENV == 'dev':
                #         print('+ [%d] Score %f > %f' % (answer, score_G1, DIAGONAL_THRESHOLD_3x3))
                # else:
                #     if ENV == 'dev':
                #         print('- [%d] Score %f < %f' % (answer, score_G1, DIAGONAL_THRESHOLD_3x3))
            print(results)
            if results != []:
                if ENV == 'dev':
                    print(results)
                if len(results) > 1 and len(results) < 8:
                    # More than one diagonal pattern detected
                    # (A*E) - (B*D) accounts for both diagonal patterns of I
                    #
                    #   * {A}  @ (B)  % [C]
                    #   % (D)  * [E]  @ {F}
                    #   @ [G]  % {H}  * (I)
                    #
                    # Pattern 2 Second Pattern Groups - *, %, @
                    print(
                        '\nMore than one diagonal pattern detected, running tiebreaker comparison . . . ')
                    # dual_pattern_image = self.OR_images(self.AND_images(a, e), self.AND_images(b, d))
                    dual_pattern_image = self.OR_images(
                        self.OR_images(a, e), self.OR_images(b, d))
                    tiebreaker_results = []
                    for ans, sc in results:
                        tiebreaker_results.append((ans, abs(self.Similarity_Check_DPR(
                            dual_pattern_image, self.Load_Image(str(ans))))))
                    print(tiebreaker_results)
                    # best_answer = max(tiebreaker_results)[1]
                    best_result = sorted(
                        tiebreaker_results, key=lambda x: x[1])[0]
                elif len(results) == 8:
                    print('\nToo many matched results, skipping...')
                    return -1, 0
                else:
                    best_result = results[0]
                if ENV == 'dev':
                    print('\nResult with highest similarity:', best_result)
                return best_result
        return -1, 0

    def Check_Diagonal_XOR_Similarity_3x3_IPR(self, images):
        a, b, c, d, e, f, g, h, i1, i2, i3, i4, i5, i6, i7, i8 = images
        answers = [i1, i2, i3, i4, i5, i6, i7, i8]

        transformation = 'Diagonal XOR Similarity IPR'
        if ENV == 'dev':
            print('SOLVING with `%s` Transformation . . . \n' % transformation)

        # Checking for Diagonal Pattern 1
        # [A] (B) {C}
        # {D} [E] (F)
        # (G) {H} [I]
        print('Checking Pattern 1 . . .\n')
        print('Step 1: Filter out differences with AND . . .\n')
        # (Group 1)
        bf = self.XOR_images(b, f)
        fg = self.XOR_images(f, g)
        bg = self.XOR_images(b, g)
        # {Group 2}
        cd = self.XOR_images(c, d)
        dh = self.XOR_images(d, h)
        ch = self.XOR_images(c, h)
        # [Group 3]
        ae = self.XOR_images(a, e)
        print('Step 2: Checking similarities with AND . . .\n')
        score_G1 = self.Similarity_Check_3x3_IPR(bf, fg, bg)
        score_G2 = self.Similarity_Check_3x3_IPR(cd, dh, ch)
        print('Score Group 1:', score_G1)
        print('Score Group 2:', score_G2)
        if score_G1 > DIAGONAL_THRESHOLD_3x3 and score_G2 > DIAGONAL_THRESHOLD_3x3:
            results = []
            for i, answer in zip(answers, range(1, len(answers)+1)):
                # [Group 3] continued
                ei = self.XOR_images(e, i)
                ai = self.XOR_images(a, i)
                score_G3 = self.Similarity_Check_3x3_IPR(ai, ei, ae)
                if score_G3 > DIAGONAL_THRESHOLD_3x3:
                    results.append((answer, score_G3))
                    if ENV == 'dev':
                        print('+ [%d] Score %f > %f' %
                              (answer, score_G3, DIAGONAL_THRESHOLD_3x3))
                else:
                    if ENV == 'dev':
                        print('- [%d] Score %f < %f' %
                              (answer, score_G3, DIAGONAL_THRESHOLD_3x3))
            if ENV == 'dev':
                print('Results:', results)
            if results != []:
                if len(results) > 1 and len(results) < 8:
                    # More than one diagonal pattern detected
                    # (A*E) - (B*D) accounts for both diagonal patterns of I
                    #
                    #   $[A] %(B) *{C}
                    #   %{D} *[E] $(F)
                    #   *(G) ${H} %[I]
                    #
                    # Pattern 1 Second Pattern Groups - *, %, @
                    print(
                        '\nMore than one diagonal pattern detected, running tiebreaker comparison . . . ')
                    dual_pattern_image = self.OR_images(
                        self.AND_images(a, e), self.AND_images(b, d))
                    # dual_pattern_image = self.OR_images(self.OR_images(a, e), self.OR_images(b, d))
                    tiebreaker_results = []
                    for ans, sc in results:
                        tiebreaker_results.append((ans, self.Similarity_Check_IPR(
                            dual_pattern_image, self.Load_Image(str(ans)))))
                    print(tiebreaker_results)
                    # best_answer = max(tiebreaker_results)[1]
                    best_result = sorted(
                        tiebreaker_results, key=lambda x: x[1])[-1]
                elif len(results) == 8:
                    print('\nToo many matched results, skipping...')
                    return -1, 0
                else:
                    best_result = results[0]
                print('\nResult with highest similarity:', best_result)
                return best_result
        # Checking for Diagonal Pattern 2
        # {A} (B) [C]
        # (D) [E] {F}
        # [G] {H} (I)
        print('Checking Pattern 2 . . .\n')
        print('Step 1: Filter out differences with AND . . .\n')
        # (Group 1)
        bd = self.XOR_images(b, d)
        # {Group 2}
        af = self.XOR_images(a, f)
        fh = self.XOR_images(f, h)
        ah = self.XOR_images(a, h)
        # [Group 3]
        ce = self.XOR_images(c, e)
        eg = self.XOR_images(e, g)
        cg = self.XOR_images(c, g)
        print('Step 2: Checking similarities with AND . . .\n')
        score_G2 = self.Similarity_Check_3x3_IPR(af, fh, ah)
        score_G3 = self.Similarity_Check_3x3_IPR(ce, eg, cg)
        print('Score Group 2:', score_G2)
        print('Score Group 3:', score_G3)
        if score_G3 > DIAGONAL_THRESHOLD_3x3 and score_G2 > DIAGONAL_THRESHOLD_3x3:
            results = []
            for i, answer in zip(answers, range(1, len(answers)+1)):
                # [Group] continued
                di = self.XOR_images(d, i)
                bi = self.XOR_images(b, i)
                score_G1 = self.Similarity_Check_3x3_IPR(bi, di, bd)

                if score_G1 > DIAGONAL_THRESHOLD_3x3:
                    results.append((answer, score_G1))
                    if ENV == 'dev':
                        print('+ [%d] Score %f > %f' %
                              (answer, score_G1, DIAGONAL_THRESHOLD_3x3))
                else:
                    if ENV == 'dev':
                        print('- [%d] Score %f < %f' %
                              (answer, score_G1, DIAGONAL_THRESHOLD_3x3))
            print(results)
            if results != []:
                if ENV == 'dev':
                    print(results)
                if len(results) > 1 and len(results) < 8:
                    # More than one diagonal pattern detected
                    # (A*E) - (B*D) accounts for both diagonal patterns of I
                    #
                    #   * {A}  @ (B)  % [C]
                    #   % (D)  * [E]  @ {F}
                    #   @ [G]  % {H}  * (I)
                    #
                    # Pattern 2 Second Pattern Groups - *, %, @
                    print(
                        '\nMore than one diagonal pattern detected, running tiebreaker comparison . . . ')
                    dual_pattern_image = self.OR_images(
                        self.AND_images(a, e), self.AND_images(b, d))
                    # dual_pattern_image = self.OR_images(self.OR_images(a, e), self.OR_images(b, d))
                    tiebreaker_results = []
                    for ans, sc in results:
                        tiebreaker_results.append((ans, abs(self.Similarity_Check_IPR(
                            dual_pattern_image, self.Load_Image(str(ans))))))
                    print(tiebreaker_results)
                    # best_answer = max(tiebreaker_results)[1]
                    best_result = sorted(
                        tiebreaker_results, key=lambda x: x[1])[-1]
                elif len(results) == 8:
                    print('\nToo many matched results, skipping...')
                    return -1, 0
                else:
                    best_result = results[0]
                if ENV == 'dev':
                    print('\nResult with highest similarity:', best_result)
                return best_result
        return -1, 0

    def Similarity_Check_DPR(self, image_a, image_b):
        list_a = [self.RGB_to_Binary(pixel)
                  for pixel in list(image_a.getdata())]
        list_b = [self.RGB_to_Binary(pixel)
                  for pixel in list(image_b.getdata())]
        # score_ipr = 100 * len([i for i, j in zip(list_a, list_b) if i == j]) / len(list_a)
        score_a_dpr = 100 * (len(list_a) - sum(list_a))/len(list_a)
        score_b_dpr = 100 * (len(list_b) - sum(list_b))/len(list_b)
        difference = score_a_dpr - score_b_dpr
        return difference  # score

    def Similarity_Check_IPR(self, image_a, image_b):
        list_a = [self.RGB_to_Binary(pixel)
                  for pixel in list(image_a.getdata())]
        list_b = [self.RGB_to_Binary(pixel)
                  for pixel in list(image_b.getdata())]
        score_ipr = 100 * \
            len([i for i, j in zip(list_a, list_b) if i == j]) / len(list_a)
        return score_ipr

    def Similarity_Check_3x3_DPR(self, image_a, image_b, image_c):
        a_and_b = self.AND_images(image_a, image_b)
        list_a_and_b = [self.RGB_to_Binary(pixel)
                        for pixel in list(a_and_b.getdata())]
        list_c = [self.RGB_to_Binary(pixel)
                  for pixel in list(image_c.getdata())]
        # score_ipr = 100 * len([i for i, j in zip(list_a_and_b, list_c) if i == j]) / len(list_a_and_b)
        score_a_and_b_dpr = 100 * \
            (len(list_a_and_b) - sum(list_a_and_b))/len(list_a_and_b)
        score_c_dpr = 100 * (len(list_c) - sum(list_c))/len(list_c)
        return score_a_and_b_dpr - score_c_dpr  # score_ipr

    def Similarity_Check_3x3_IPR(self, image_a, image_b, image_c):
        a_and_b = self.AND_images(image_a, image_b)
        list_a_and_b = [self.RGB_to_Binary(pixel)
                        for pixel in list(a_and_b.getdata())]
        list_c = [self.RGB_to_Binary(pixel)
                  for pixel in list(image_c.getdata())]
        score_ipr = 100 * \
            len([i for i, j in zip(list_a_and_b, list_c) if i == j]) / \
            len(list_a_and_b)
        return score_ipr

    def Figure_Count_Pattern_3x3_Answer(self):
        # im_a, im_b, im_c, im_d, im_e, im_f, im_g, im_h = images
        transformation = 'Figure Count Pattern'
        if ENV == 'dev':
            print('SOLVING with `%s` Transformation . . . \n' % transformation)

        imageData = {}
        for key, value in sorted(self.problem.figures.items()):
            figureObjects = value.objects
            imageData[key] = len(figureObjects)
        try:
            FigureCoeff_AC = imageData['C'] // imageData['A']
            FigureCoeff_DF = imageData['F'] // imageData['D']

            if imageData['C'] == FigureCoeff_AC * imageData['A'] and imageData['F'] == FigureCoeff_DF * imageData['D']:
                if ENV == 'dev':
                    print(
                        'Figure Count multiplies by %d right to left . . . \n' % FigureCoeff_AC)
                for i in range(1, self.num_options+1):
                    figure_i = imageData[str(i)]
                    FigureCoeff_GI = figure_i // imageData['G']
                    if FigureCoeff_GI == FigureCoeff_AC:
                        return i
        except ZeroDivisionError:
            return -1

    def Get_AND_3x3_Answer_DPR(self, images):
        im_a, im_b, im_c, im_d, im_e, im_f, im_g, im_h = images
        transformation = 'AND Images DPR'
        if ENV == 'dev':
            print('SOLVING with `%s` Transformation . . . \n' % transformation)

        # Score_H_ABC = self.PixelCompare_3x3(self.AND_images(im_a, im_b), im_c, transformation)
        # Score_H_DEF = self.PixelCompare_3x3(self.AND_images(im_d, im_e), im_f, transformation)

        # Score_V_ADG = self.PixelCompare_3x3(self.AND_images(im_a, im_d), im_g, transformation)
        # Score_V_BEH = self.PixelCompare_3x3(self.AND_images(im_b, im_e), im_h, transformation)

        Difference_H_ABC = self.Similarity_Check_DPR(
            self.AND_images(im_a, im_b), im_c)
        Difference_H_DEF = self.Similarity_Check_DPR(
            self.AND_images(im_d, im_e), im_f)

        Difference_V_ADG = self.Similarity_Check_DPR(
            self.AND_images(im_a, im_d), im_g)
        Difference_V_BEH = self.Similarity_Check_DPR(
            self.AND_images(im_b, im_e), im_h)

        # if ENV == 'dev':
        #     print('Score_H_ABC:', Score_H_ABC)
        #     print('Score_H_DEF:', Score_H_DEF)
        #     print('Score_V_ADG:', Score_V_ADG)
        #     print('Score_V_BEH:', Score_V_BEH)
        if ENV == 'dev':
            print('Difference_H_ABC:', Difference_H_ABC)
            print('Difference_H_DEF:', Difference_H_DEF)
            print('Difference_V_ADG:', Difference_V_ADG)
            print('Difference_V_BEH:', Difference_V_BEH)
        # if Score_H_ABC > Score_V_ADG:
        if abs(Difference_H_ABC) < abs(Difference_V_ADG) and abs(Difference_H_DEF) < abs(Difference_V_BEH):
            if ENV == 'dev':
                print('Horizontal is stronger . . . \n')
            # if Score_H_ABC > AND_THRESHOLD_3x3 and Score_H_DEF > AND_THRESHOLD_3x3:
            if abs(Difference_H_ABC) < abs(DIFFERENCE_THRESHOLD) and abs(Difference_H_DEF) < abs(DIFFERENCE_THRESHOLD):
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    # score = self.PixelCompare_3x3(self.AND_images(im_g, im_h), im_i, transformation)
                    difference = self.Similarity_Check_DPR(
                        self.AND_images(im_g, im_h), im_i)
                    # if score > AND_THRESHOLD_3x3:
                    if abs(difference) < DIFFERENCE_THRESHOLD:
                        # print('-- Score_H_GHI:', score, '--\n')
                        print('-- Difference_H_GHI:', difference, '--\n')
                        # results.append((i, score))
                        results.append((i, abs(difference)))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    # return sorted(results, key=lambda x: x[1])[len(results)-1]
                    return sorted(results, key=lambda x: x[1])[0]
                return -1, 0
            else:
                print('No match...')
        else:
            if ENV == 'dev':
                print('Vertical is stronger . . . \n')
            # if Score_V_ADG > AND_THRESHOLD_3x3 and Score_V_BEH > AND_THRESHOLD_3x3:
            if abs(Difference_V_ADG) < DIFFERENCE_THRESHOLD and abs(Difference_V_BEH) < DIFFERENCE_THRESHOLD:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    # score = self.PixelCompare_3x3(self.AND_images(im_c, im_f), im_i, transformation)
                    difference = self.Similarity_Check_DPR(
                        self.AND_images(im_c, im_f), im_i)
                    # if score > AND_THRESHOLD_3x3:
                    if abs(difference) < DIFFERENCE_THRESHOLD:
                        # print('-- Score_V_CFI:', score, '--\n')
                        print('-- Difference_V_CFI:', difference, '--\n')
                        # results.append((i, score))
                        results.append((i, abs(difference)))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    # return sorted(results, key=lambda x: x[1])[len(results)-1]
                    return sorted(results, key=lambda x: x[1])[0]
                return -1, 0
            else:
                print('No match...')
        return -1, 0

    def Get_AND_3x3_Answer_IPR(self, images):
        im_a, im_b, im_c, im_d, im_e, im_f, im_g, im_h = images
        transformation = 'AND Images IPR'
        if ENV == 'dev':
            print('SOLVING with `%s` Transformation . . . \n' % transformation)

        Score_H_ABC = self.Similarity_Check_IPR(
            self.AND_images(im_a, im_b), im_c)
        Score_H_DEF = self.Similarity_Check_IPR(
            self.AND_images(im_d, im_e), im_f)

        Score_V_ADG = self.Similarity_Check_IPR(
            self.AND_images(im_a, im_d), im_g)
        Score_V_BEH = self.Similarity_Check_IPR(
            self.AND_images(im_b, im_e), im_h)

        if ENV == 'dev':
            print('Score_H_ABC:', Score_H_ABC)
            print('Score_H_DEF:', Score_H_DEF)
            print('Score_V_ADG:', Score_V_ADG)
            print('Score_V_BEH:', Score_V_BEH)
        if Score_H_ABC > Score_V_ADG:
            if ENV == 'dev':
                print('Horizontal is stronger . . . \n')
            if Score_H_ABC > AND_THRESHOLD_3x3 and Score_H_DEF > AND_THRESHOLD_3x3:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    score = self.Similarity_Check_IPR(
                        self.AND_images(im_g, im_h), im_i)
                    if score > AND_THRESHOLD_3x3:
                        print('-- Score_H_GHI:', score, '--\n')
                        results.append((i, score))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    return sorted(results, key=lambda x: x[1])[-1]
                return -1, 0
            else:
                print('No match...')
        else:
            if ENV == 'dev':
                print('Vertical is stronger . . . \n')
            if Score_V_ADG > AND_THRESHOLD_3x3 and Score_V_BEH > AND_THRESHOLD_3x3:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    score = self.Similarity_Check_IPR(
                        self.AND_images(im_c, im_f), im_i)
                    if score > AND_THRESHOLD_3x3:
                        print('-- Score_V_CFI:', score, '--\n')
                        results.append((i, score))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    return sorted(results, key=lambda x: x[1])[-1]
                return -1, 0
            else:
                print('No match...')
        return -1, 0

    def Get_OR_3x3_Answer_DPR(self, images):
        im_a, im_b, im_c, im_d, im_e, im_f, im_g, im_h = images
        transformation = 'OR Images DPR'
        if ENV == 'dev':
            print('SOLVING with `%s` Transformation . . . \n' % transformation)

        Difference_H_ABC = self.Similarity_Check_DPR(
            self.OR_images(im_a, im_b), im_c)
        Difference_H_DEF = self.Similarity_Check_DPR(
            self.OR_images(im_d, im_e), im_f)

        Difference_V_ADG = self.Similarity_Check_DPR(
            self.OR_images(im_a, im_d), im_g)
        Difference_V_BEH = self.Similarity_Check_DPR(
            self.OR_images(im_b, im_e), im_h)

        if ENV == 'dev':
            print('Difference_H_ABC:', Difference_H_ABC)
            print('Difference_H_DEF:', Difference_H_DEF)
            print('Difference_V_ADG:', Difference_V_ADG)
            print('Difference_V_BEH:', Difference_V_BEH)
        if abs(Difference_H_ABC) < Difference_V_ADG and abs(Difference_H_DEF) < Difference_V_BEH:
            if ENV == 'dev':
                print('Horizontal is stronger . . . \n')
            if abs(Difference_H_ABC) < DIFFERENCE_THRESHOLD and abs(Difference_H_DEF) < DIFFERENCE_THRESHOLD:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    difference = self.Similarity_Check_DPR(
                        self.OR_images(im_g, im_h), im_i)
                    if abs(difference) < DIFFERENCE_THRESHOLD:
                        print('-- Difference_H_GHI:', difference, '--\n')
                        results.append((i, abs(difference)))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    return sorted(results, key=lambda x: x[1])[0]
                return -1, 0
            else:
                print('No match...')
        else:
            if ENV == 'dev':
                print('Vertical is stronger . . . \n')
            if abs(Difference_V_ADG) < DIFFERENCE_THRESHOLD and abs(Difference_V_BEH) < DIFFERENCE_THRESHOLD:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    difference = self.Similarity_Check_DPR(
                        self.OR_images(im_c, im_f), im_i)
                    if abs(difference) < DIFFERENCE_THRESHOLD:
                        print('-- Difference_V_CFI:', difference, '--\n')
                        results.append((i, abs(difference)))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    return sorted(results, key=lambda x: x[1])[0]
                return -1, 0
            else:
                print('No match...')
        return -1, 0

    def Get_OR_3x3_Answer_IPR(self, images):
        im_a, im_b, im_c, im_d, im_e, im_f, im_g, im_h = images
        transformation = 'OR Images IPR'
        if ENV == 'dev':
            print('SOLVING with `%s` Transformation . . . \n' % transformation)

        Score_H_ABC = self.Similarity_Check_IPR(
            self.OR_images(im_a, im_b), im_c)
        Score_H_DEF = self.Similarity_Check_IPR(
            self.OR_images(im_d, im_e), im_f)

        Score_V_ADG = self.Similarity_Check_IPR(
            self.OR_images(im_a, im_d), im_g)
        Score_V_BEH = self.Similarity_Check_IPR(
            self.OR_images(im_b, im_e), im_h)

        if ENV == 'dev':
            print('Score_H_ABC:', Score_H_ABC)
            print('Score_V_ADG:', Score_V_ADG)
        if Score_H_ABC > Score_V_ADG:
            if ENV == 'dev':
                print('Horizontal is stronger . . . \n')
            if Score_H_ABC > OR_THRESHOLD_3x3 and Score_H_DEF > OR_THRESHOLD_3x3:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    score = self.Similarity_Check_IPR(
                        self.OR_images(im_g, im_h), im_i)
                    if score > OR_THRESHOLD_3x3:
                        print('-- Score_H_GHI:', score, '--\n')
                        results.append((i, score))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    return sorted(results, key=lambda x: x[1])[len(results)-1]
                return -1, 0
            else:
                print('No match...')
        else:
            if ENV == 'dev':
                print('Vertical is stronger . . . \n')
            if Score_V_ADG > OR_THRESHOLD_3x3 and Score_V_BEH > OR_THRESHOLD_3x3:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    score = self.Similarity_Check_IPR(
                        self.OR_images(im_c, im_f), im_i)
                    if score > OR_THRESHOLD_3x3:
                        print('-- Score_V_CFI:', score, '--\n')
                        results.append((i, score))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    return sorted(results, key=lambda x: x[1])[len(results)-1]
                return -1, 0
            else:
                print('No match...')
        return -1, 0

    def Get_XOR_3x3_Answer_DPR(self, images):
        im_a, im_b, im_c, im_d, im_e, im_f, im_g, im_h = images
        transformation = 'XOR Images DPR'
        if ENV == 'dev':
            print('SOLVING with `%s` Transformation . . . \n' % transformation)

        # Horizontal Differences
        # Row 1
        ab = self.XOR_images(im_a, im_b)
        bc = self.XOR_images(im_b, im_c)
        ac = self.XOR_images(im_a, im_c)
        # Row 2
        de = self.XOR_images(im_d, im_e)
        ef = self.XOR_images(im_e, im_f)
        df = self.XOR_images(im_d, im_f)
        # Row 3
        gh = self.XOR_images(im_g, im_h)

        # Vertical Differences
        # Column 1
        ad = self.XOR_images(im_a, im_d)
        dg = self.XOR_images(im_d, im_g)
        ag = self.XOR_images(im_a, im_g)
        # Column 2
        be = self.XOR_images(im_b, im_e)
        bh = self.XOR_images(im_b, im_h)
        eh = self.XOR_images(im_e, im_h)
        # Column 3
        cf = self.XOR_images(im_c, im_f)

        # Score_H_ABC = self.Similarity_Check_3x3(ab, bc, ac)
        # Score_H_DEF = self.Similarity_Check_3x3(de, ef, df)

        # Score_V_ADG = self.Similarity_Check_3x3(ad, dg, ag)
        # Score_V_BEH = self.Similarity_Check_3x3(be, bh, eh)

        Difference_H_ABC = self.Similarity_Check_3x3_DPR(ab, bc, ac)
        Difference_H_DEF = self.Similarity_Check_3x3_DPR(de, ef, df)

        Difference_V_ADG = self.Similarity_Check_3x3_DPR(ad, dg, ag)
        Difference_V_BEH = self.Similarity_Check_3x3_DPR(be, bh, eh)

        # if ENV == 'dev':
        #     print('Score_H_ABC:', Score_H_ABC)
        #     print('Score_V_ADG:', Score_V_ADG)
        if ENV == 'dev':
            print('Difference_H_ABC:', Difference_H_ABC)
            print('Difference_V_ADG:', Difference_V_ADG)
        # if Score_H_ABC > Score_V_ADG:
        if abs(Difference_H_ABC) < abs(Difference_V_ADG) and abs(Difference_H_DEF) < abs(Difference_V_BEH):
            if ENV == 'dev':
                print('Horizontal is stronger . . . \n')
            # if Score_H_ABC > XOR_THRESHOLD_3x3 and Score_H_DEF > XOR_THRESHOLD_3x3:
            if abs(Difference_H_ABC) < DIFFERENCE_THRESHOLD and abs(Difference_H_DEF) < DIFFERENCE_THRESHOLD:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    hi = self.XOR_images(im_h, im_i)
                    gi = self.XOR_images(im_g, im_i)
                    # score = self.Similarity_Check_3x3(hi, gi, gh)
                    difference = self.Similarity_Check_3x3_DPR(hi, gi, gh)
                    # if score > XOR_THRESHOLD_3x3:
                    if abs(difference) < DIFFERENCE_THRESHOLD:
                        # print('-- Score_H_GHI:', score, '--\n')
                        print('-- Difference_H_GHI:', difference, '--\n')
                        # results.append((i, score))
                        results.append((i, abs(difference)))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    # return sorted(results, key=lambda x: x[1])[len(results)-1]
                    return sorted(results, key=lambda x: x[1])[0]
                return -1, 0
            else:
                print('No match...')
        else:
            if ENV == 'dev':
                print('Vertical is stronger . . . \n')
            # if Score_V_ADG > XOR_THRESHOLD_3x3 and Score_V_BEH > XOR_THRESHOLD_3x3:
            if abs(Difference_V_ADG) < DIFFERENCE_THRESHOLD and abs(Difference_V_BEH) < DIFFERENCE_THRESHOLD:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    fi = self.XOR_images(im_f, im_i)
                    ci = self.XOR_images(im_c, im_i)
                    # score = self.Similarity_Check_3x3(ci, fi, cf)
                    difference = self.Similarity_Check_3x3_DPR(ci, fi, cf)
                    # if score > XOR_THRESHOLD_3x3:
                    if abs(difference) < DIFFERENCE_THRESHOLD:
                        # print('-- Score_V_CFI:', score, '--\n')
                        print('-- Difference_V_CFI:', difference, '--\n')
                        # results.append((i, score))
                        results.append((i, abs(difference)))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    # return sorted(results, key=lambda x: x[1])[len(results)-1]
                    return sorted(results, key=lambda x: x[1])[0]
                return -1, 0
            else:
                print('No match...')
        return -1, 0

    def Get_XOR_3x3_Answer_IPR(self, images):
        im_a, im_b, im_c, im_d, im_e, im_f, im_g, im_h = images
        transformation = 'XOR Images IPR'
        if ENV == 'dev':
            print('SOLVING with `%s` Transformation . . . \n' % transformation)

        # Horizontal Differences
        # Row 1
        ab = self.XOR_images(im_a, im_b)
        bc = self.XOR_images(im_b, im_c)
        ac = self.XOR_images(im_a, im_c)
        # Row 2
        de = self.XOR_images(im_d, im_e)
        ef = self.XOR_images(im_e, im_f)
        df = self.XOR_images(im_d, im_f)
        # Row 3
        gh = self.XOR_images(im_g, im_h)

        # Vertical Differences
        # Column 1
        ad = self.XOR_images(im_a, im_d)
        dg = self.XOR_images(im_d, im_g)
        ag = self.XOR_images(im_a, im_g)
        # Column 2
        be = self.XOR_images(im_b, im_e)
        bh = self.XOR_images(im_b, im_h)
        eh = self.XOR_images(im_e, im_h)
        # Column 3
        cf = self.XOR_images(im_c, im_f)

        Score_H_ABC = self.Similarity_Check_3x3_IPR(ab, bc, ac)
        Score_H_DEF = self.Similarity_Check_3x3_IPR(de, ef, df)

        Score_V_ADG = self.Similarity_Check_3x3_IPR(ad, dg, ag)
        Score_V_BEH = self.Similarity_Check_3x3_IPR(be, bh, eh)

        if ENV == 'dev':
            print('Score_H_ABC:', Score_H_ABC)
            print('Score_V_ADG:', Score_V_ADG)
        if Score_H_ABC > Score_V_ADG:
            if ENV == 'dev':
                print('Horizontal is stronger . . . \n')
            if Score_H_ABC > XOR_THRESHOLD_3x3 and Score_H_DEF > XOR_THRESHOLD_3x3:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    hi = self.XOR_images(im_h, im_i)
                    gi = self.XOR_images(im_g, im_i)
                    score = self.Similarity_Check_3x3_IPR(hi, gi, gh)
                    if score > XOR_THRESHOLD_3x3:
                        print('-- Score_H_GHI:', score, '--\n')
                        results.append((i, score))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    # return sorted(results, key=lambda x: x[1])[len(results)-1]
                    return sorted(results, key=lambda x: x[1])[-1]
                return -1, 0
            else:
                print('No match...')
        else:
            if ENV == 'dev':
                print('Vertical is stronger . . . \n')
            if Score_V_ADG > XOR_THRESHOLD_3x3 and Score_V_BEH > XOR_THRESHOLD_3x3:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    fi = self.XOR_images(im_f, im_i)
                    ci = self.XOR_images(im_c, im_i)
                    score = self.Similarity_Check_3x3_IPR(ci, fi, cf)
                    if score > XOR_THRESHOLD_3x3:
                        print('-- Score_V_CFI:', score, '--\n')
                        results.append((i, score))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    # return sorted(results, key=lambda x: x[1])[len(results)-1]
                    return sorted(results, key=lambda x: x[1])[-1]
                return -1, 0
            else:
                print('No match...')
        return -1, 0

    def Get_Simple_XOR_3x3_Answer_DPR(self, images):
        im_a, im_b, im_c, im_d, im_e, im_f, im_g, im_h = images
        transformation = 'Simple XOR Images DPR'
        if ENV == 'dev':
            print('SOLVING with `%s` Transformation . . . \n' % transformation)

        Difference_H_ABC = self.Similarity_Check_DPR(
            self.XOR_images(im_a, im_b), im_c)
        Difference_H_DEF = self.Similarity_Check_DPR(
            self.XOR_images(im_d, im_e), im_f)

        Difference_V_ADG = self.Similarity_Check_DPR(
            self.XOR_images(im_a, im_d), im_g)
        Difference_V_BEH = self.Similarity_Check_DPR(
            self.XOR_images(im_b, im_e), im_h)

        if ENV == 'dev':
            print('Difference_H_ABC:', Difference_H_ABC)
            print('Difference_V_ADG:', Difference_V_ADG)
        if abs(Difference_H_ABC) < abs(Difference_V_ADG) and abs(Difference_H_DEF) < abs(Difference_V_BEH):
            if ENV == 'dev':
                print('Horizontal is stronger . . . \n')
            if abs(Difference_H_ABC) < DIFFERENCE_THRESHOLD and abs(Difference_H_DEF) < DIFFERENCE_THRESHOLD:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    difference = self.Similarity_Check_DPR(
                        self.XOR_images(im_g, im_h), im_i)
                    if abs(difference) < DIFFERENCE_THRESHOLD:
                        print('-- Difference_H_GHI:', difference, '--\n')
                        results.append((i, abs(difference)))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    return sorted(results, key=lambda x: x[1])[0]
                return -1, 0
            else:
                print('No match...')
        else:
            if ENV == 'dev':
                print('Vertical is stronger . . . \n')
            if abs(Difference_V_ADG) < DIFFERENCE_THRESHOLD and abs(Difference_V_BEH) < DIFFERENCE_THRESHOLD:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    difference = self.Similarity_Check_DPR(
                        self.XOR_images(im_c, im_f), im_i)
                    if abs(difference) < DIFFERENCE_THRESHOLD:
                        print('-- Difference_V_CFI:', difference, '--\n')
                        results.append((i, abs(difference)))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    return sorted(results, key=lambda x: x[1])[0]
                return -1, 0
            else:
                print('No match...')
        return -1, 0

    def Get_Simple_XOR_3x3_Answer_IPR(self, images):
        im_a, im_b, im_c, im_d, im_e, im_f, im_g, im_h = images
        transformation = 'Simple XOR Images IPR'
        if ENV == 'dev':
            print('SOLVING with `%s` Transformation . . . \n' % transformation)

        Score_H_ABC = self.Similarity_Check_IPR(
            self.XOR_images(im_a, im_b), im_c)
        Score_H_DEF = self.Similarity_Check_IPR(
            self.XOR_images(im_d, im_e), im_f)

        Score_V_ADG = self.Similarity_Check_IPR(
            self.XOR_images(im_a, im_d), im_g)
        Score_V_BEH = self.Similarity_Check_IPR(
            self.XOR_images(im_b, im_e), im_h)

        if ENV == 'dev':
            print('Score_H_ABC:', Score_H_ABC)
            print('Score_V_ADG:', Score_V_ADG)
        if Score_H_ABC > Score_V_ADG and Score_H_DEF > Score_V_BEH:
            if ENV == 'dev':
                print('Horizontal is stronger . . . \n')
            if Score_H_ABC > XOR_THRESHOLD_3x3 and Score_H_DEF > XOR_THRESHOLD_3x3:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    score = self.Similarity_Check_IPR(
                        self.XOR_images(im_g, im_h), im_i)
                    if score > XOR_THRESHOLD_3x3:
                        print('-- Score_H_GHI:', score, '--\n')
                        results.append((i, score))
                    else:
                        print('Score_H_GHI %d < THRESHOLD %f\n' %
                              (score, XOR_THRESHOLD_3x3))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    return sorted(results, key=lambda x: x[1])[-1]
                return -1, 0
            else:
                print('No match...')
        else:
            if ENV == 'dev':
                print('Vertical is stronger . . . \n')
            if Score_V_ADG > XOR_THRESHOLD_3x3 and Score_V_BEH > XOR_THRESHOLD_3x3:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    score = self.Similarity_Check_IPR(
                        self.XOR_images(im_c, im_f), im_i)
                    if score > XOR_THRESHOLD_3x3:
                        print('-- Score_V_CFI:', score, '--\n')
                        results.append((i, score))
                    else:
                        print('Score_H_CFI %d < THRESHOLD %f\n' %
                              (score, XOR_THRESHOLD_3x3))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    return sorted(results, key=lambda x: x[1])[-1]
                return -1, 0
            else:
                print('No match...')
        return -1, 0

    def Get_Subtract_3x3_Answer_DPR(self, images):
        im_a, im_b, im_c, im_d, im_e, im_f, im_g, im_h = images
        transformation = 'Subtract Images DPR'
        if ENV == 'dev':
            print('SOLVING with `%s` Transformation . . . \n' % transformation)

        list_c = [self.RGB_to_Binary(pixel) for pixel in list(im_c.getdata())]
        TOTAL_PIXELS = len(list_c)
        list_f = [self.RGB_to_Binary(pixel) for pixel in list(im_f.getdata())]
        list_g = [self.RGB_to_Binary(pixel) for pixel in list(im_g.getdata())]
        list_h = [self.RGB_to_Binary(pixel) for pixel in list(im_h.getdata())]

        # Horizontal DPR Ratios
        ratio_a_b_dpr = self.Subtract_images_DPR(im_a, im_b)
        ratio_d_e_dpr = self.Subtract_images_DPR(im_d, im_e)
        ratio_g_h_dpr = self.Subtract_images_DPR(im_g, im_h)

        # Vertical DPR Ratios
        ratio_a_d_dpr = self.Subtract_images_DPR(im_a, im_d)
        ratio_b_e_dpr = self.Subtract_images_DPR(im_b, im_e)
        ratio_c_f_dpr = self.Subtract_images_DPR(im_c, im_f)

        # Comparison DPR Ratios
        ratio_c_dpr = 100 * (TOTAL_PIXELS - sum(list_c))/TOTAL_PIXELS
        ratio_f_dpr = 100 * (TOTAL_PIXELS - sum(list_f))/TOTAL_PIXELS
        ratio_g_dpr = 100 * (TOTAL_PIXELS - sum(list_g))/TOTAL_PIXELS
        ratio_h_dpr = 100 * (TOTAL_PIXELS - sum(list_h))/TOTAL_PIXELS

        Difference_H_ABC = ratio_a_b_dpr - ratio_c_dpr
        Difference_H_DEF = ratio_d_e_dpr - ratio_f_dpr

        Difference_V_ADG = ratio_a_d_dpr - ratio_g_dpr
        Difference_V_BEH = ratio_b_e_dpr - ratio_h_dpr

        if ENV == 'dev':
            print('Difference_H_ABC:', Difference_H_ABC)
            print('Difference_V_ADG:', Difference_V_ADG)
        if abs(Difference_H_ABC) < abs(Difference_V_ADG) and abs(Difference_H_DEF) < abs(Difference_V_BEH):
            if ENV == 'dev':
                print('Horizontal is stronger . . . \n')
            if abs(Difference_H_ABC) < DIFFERENCE_THRESHOLD and abs(Difference_H_DEF) < DIFFERENCE_THRESHOLD:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    list_i = [self.RGB_to_Binary(pixel)
                              for pixel in list(im_i.getdata())]
                    ratio_i_dpr = 100 * \
                        (TOTAL_PIXELS - sum(list_i))/TOTAL_PIXELS
                    difference = ratio_g_h_dpr - ratio_i_dpr
                    if abs(difference) < DIFFERENCE_THRESHOLD:
                        print('-- Difference_H_GHI:', difference, '--\n')
                        results.append((i, abs(difference)))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    if len(results) > 1:
                        print(
                            '\nMore than one result from DPR, running IPR comparison . . . ')
                        Score_H_ABC = self.Similarity_Check_IPR(
                            self.Subtract_images_IPR(im_a, im_b), im_c)
                        Score_H_DEF = self.Similarity_Check_IPR(
                            self.Subtract_images_IPR(im_c, im_e), im_f)

                        Score_V_ADG = self.Similarity_Check_IPR(
                            self.Subtract_images_IPR(im_a, im_d), im_g)
                        Score_V_BEH = self.Similarity_Check_IPR(
                            self.Subtract_images_IPR(im_b, im_e), im_h)
                        ipr_results = []
                        for i, difference in results:
                            im_i = self.Load_Image(str(i))
                            if Score_H_ABC > Score_V_ADG and Score_H_DEF > Score_V_BEH:
                                print('Horizontal is stronger . . . \n')
                                ipr_results.append((i, self.Similarity_Check_IPR(
                                    self.Subtract_images_IPR(im_g, im_h), im_i)))
                            else:
                                print('Vertical is stronger . . . \n')
                                ipr_results.append((i, self.Similarity_Check_IPR(
                                    self.Subtract_images_IPR(im_c, im_f), im_i)))
                        print(ipr_results)
                        return sorted(ipr_results, key=lambda x: x[1])[-1]
                    return sorted(results, key=lambda x: x[1])[0]
                return -1, 0
            else:
                print('No match...')
        else:
            if ENV == 'dev':
                print('Vertical is stronger . . . \n')
            if abs(Difference_V_ADG) < DIFFERENCE_THRESHOLD and abs(Difference_V_BEH) < DIFFERENCE_THRESHOLD:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    list_i = [self.RGB_to_Binary(pixel)
                              for pixel in list(im_i.getdata())]
                    ratio_i_dpr = 100 * \
                        (TOTAL_PIXELS - sum(list_i))/TOTAL_PIXELS
                    difference = ratio_c_f_dpr - ratio_i_dpr
                    if abs(difference) < DIFFERENCE_THRESHOLD:
                        print('-- Difference_V_CFI:', difference, '--\n')
                        results.append((i, abs(difference)))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    if len(results) > 1:
                        print(
                            '\nMore than one result from DPR, running IPR comparison . . . ')
                        Score_H_ABC = self.Similarity_Check_IPR(
                            self.Subtract_images_IPR(im_a, im_b), im_c)
                        Score_H_DEF = self.Similarity_Check_IPR(
                            self.Subtract_images_IPR(im_c, im_e), im_f)

                        Score_V_ADG = self.Similarity_Check_IPR(
                            self.Subtract_images_IPR(im_a, im_d), im_g)
                        Score_V_BEH = self.Similarity_Check_IPR(
                            self.Subtract_images_IPR(im_b, im_e), im_h)
                        ipr_results = []
                        for i, difference in results:
                            im_i = self.Load_Image(str(i))
                            if Score_H_ABC > Score_V_ADG and Score_H_DEF > Score_V_BEH:
                                print('Horizontal is stronger . . . \n')
                                ipr_results.append((i, self.Similarity_Check_IPR(
                                    self.Subtract_images_IPR(im_g, im_h), im_i)))
                            else:
                                print('Vertical is stronger . . . \n')
                                ipr_results.append((i, self.Similarity_Check_IPR(
                                    self.Subtract_images_IPR(im_c, im_f), im_i)))
                        return sorted(ipr_results, key=lambda x: x[1])[-1]
                    return sorted(results, key=lambda x: x[1])[0]
                return -1, 0
            else:
                print('No match...')
        return -1, 0

    def Get_Subtract_3x3_Answer_IPR(self, images):
        im_a, im_b, im_c, im_d, im_e, im_f, im_g, im_h = images
        transformation = 'Subtract Images IPR'
        if ENV == 'dev':
            print('SOLVING with `%s` Transformation . . . \n' % transformation)

        Score_H_ABC = self.Similarity_Check_IPR(
            self.Subtract_images_IPR(im_a, im_b), im_c)
        Score_H_DEF = self.Similarity_Check_IPR(
            self.Subtract_images_IPR(im_c, im_e), im_f)

        Score_V_ADG = self.Similarity_Check_IPR(
            self.Subtract_images_IPR(im_a, im_d), im_g)
        Score_V_BEH = self.Similarity_Check_IPR(
            self.Subtract_images_IPR(im_b, im_e), im_h)

        if ENV == 'dev':
            print('Score_H_ABC:', Score_H_ABC)
            print('Score_V_ADG:', Score_V_ADG)
        if Score_H_ABC > Score_V_ADG and Score_H_DEF > Score_V_BEH:
            if ENV == 'dev':
                print('Horizontal is stronger . . . \n')
            if Score_H_ABC > SUBTRACT_THRESHOLD_3x3 and Score_H_DEF > SUBTRACT_THRESHOLD_3x3:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    score = self.Similarity_Check_IPR(
                        self.Subtract_images_IPR(im_g, im_h), im_i)
                    if score > SUBTRACT_THRESHOLD_3x3:
                        print('-- Difference_H_GHI:', score, '--\n')
                        results.append((i, 100-score))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    return sorted(results, key=lambda x: x[1])[0]
                return -1, 0
            else:
                print('No match...')
        else:
            if ENV == 'dev':
                print('Vertical is stronger . . . \n')
            if Score_V_ADG > SUBTRACT_THRESHOLD_3x3 and Score_V_BEH > SUBTRACT_THRESHOLD_3x3:
                results = []
                for i in range(1, self.num_options+1):
                    im_i = self.Load_Image(str(i))
                    score = self.Similarity_Check_IPR(
                        self.Subtract_images_IPR(im_c, im_f), im_i)
                    if score > SUBTRACT_THRESHOLD_3x3:
                        print('-- Difference_V_CFI:', score, '--\n')
                        results.append((i, 100-score))
                print(results)
                if ENV == 'dev':
                    input()
                if results != []:
                    return sorted(results, key=lambda x: x[1])[0]
                return -1, 0
            else:
                print('No match...')
        return -1, 0

    def Subtract_images_DPR(self, image_a, image_b):
        list_a = [self.RGB_to_Binary(pixel)
                  for pixel in list(image_a.getdata())]
        list_b = [self.RGB_to_Binary(pixel)
                  for pixel in list(image_b.getdata())]
        sum_a_dpr = (len(list_a) - sum(list_a))
        sum_b_dpr = (len(list_b) - sum(list_b))

        # Returns the ratio of the difference of dark pixels between A and B and the total number of pixels
        ratio_a_b_dpr = 100 * abs(sum_a_dpr - sum_b_dpr) / len(list_a)
        return ratio_a_b_dpr

    def Subtract_images_IPR(self, image_a, image_b):
        return ImageChops.invert(self.OR_images(ImageChops.invert(image_a), image_b))

    def Duplicate_Check(self, image_a, image_b):
        return ImageChops.difference(image_a, image_b).getbbox() is None

    def Transformation_Dict(self):
        return {
            'None': 'None',
            '0': 'Horizontal Flip',
            '1': 'Vertical Flip',
            'Rotate 45': 'Rotate 45',
            '2': 'Rotate 90',
            'Rotate 135': 'Rotate 135',
            '3': 'Rotate 180',
            'Rotate 225': 'Rotate 225',
            '4': 'Rotate 270',
            'Rotate 315': 'Rotate 315',
            'XOR Images': 'XOR Images',
            'OR Images': 'OR Images',
            'AND Images': 'AND Images',
            'Apply Difference': 'Apply Difference'
        }

    def Threshold_Dict(self):
        return {
            'None': IMAGE_NONE_THRESHOLD,
            'Horizontal Flip': IMAGE_TRANSPOSE_THRESHOLD,
            'Vertical Flip': IMAGE_TRANSPOSE_THRESHOLD,
            'Rotate 45': IMAGE_TRANSPOSE_THRESHOLD,
            'Rotate 90': IMAGE_TRANSPOSE_THRESHOLD,
            'Rotate 135': IMAGE_TRANSPOSE_THRESHOLD,
            'Rotate 180': IMAGE_TRANSPOSE_THRESHOLD,
            'Rotate 225': IMAGE_TRANSPOSE_THRESHOLD,
            'Rotate 270': IMAGE_TRANSPOSE_THRESHOLD,
            'Rotate 315': IMAGE_TRANSPOSE_THRESHOLD,
            'XOR Images': XOR_THRESHOLD,
            'OR Images': OR_THRESHOLD,
            'AND Images': AND_THRESHOLD,
            'Apply Difference': APPLY_DIFFERENCE_THRESHOLD
        }

    def PixelCompare(self, image_a, image_b, transformation, transformations_done):
        if transformation is None:
            # no transformation
            list_a = [self.RGB_to_Binary(pixel)
                      for pixel in list(image_a.getdata())]
            list_b = [self.RGB_to_Binary(pixel)
                      for pixel in list(image_b.getdata())]

            score_pixel = 100 * \
                len([i for i, j in zip(list_a, list_b) if i == j]) / len(list_a)
            # score_rms = self.RMS_Difference(image_a, image_b) / 1000
        elif 'Rotate' in str(transformation):
            list_a = [self.RGB_to_Binary(pixel) for pixel in list(
                self.Rotate_Image(image_a, transformation.split(' ')[1]).getdata())]
            list_b = [self.RGB_to_Binary(pixel)
                      for pixel in list(image_b.getdata())]

            score_pixel = 100 * \
                len([i for i, j in zip(list_a, list_b) if i == j]) / len(list_a)
        elif transformation == 'XOR Images':
            image_a_XOR_b = self.XOR_images(image_a, image_b)
            list_a_XOR_b = [self.RGB_to_Binary(
                pixel) for pixel in list(image_a_XOR_b.getdata())]
            list_a = [self.RGB_to_Binary(pixel)
                      for pixel in list(image_a.getdata())]
            list_b = [self.RGB_to_Binary(pixel)
                      for pixel in list(image_b.getdata())]

            score_pixel_a = 100 * \
                len([i for i, j in zip(list_a_XOR_b, list_a) if i == j]) / len(list_a)
            score_pixel_b = 100 * \
                len([i for i, j in zip(list_a_XOR_b, list_b) if i == j]) / len(list_a)

            if not self.readyForSecondaryCompare:
                # if self.problem.name == 'Basic Problem B-11':
                #     image_a_XOR_b.show()
                #     image_a.show()
                #     image_b.show()
                #     input()

                if score_pixel_a > score_pixel_b:
                    print("Reverse XOR order works better! %f > %f" %
                          (score_pixel_a, score_pixel_b))
                    score_pixel = score_pixel_a
                    # score_rms = self.RMS_Difference(image_a_XOR_b, image_a) / 1000
                    self.toggleDirection = True
                else:
                    print("Standard XOR order works better! %f >= %f" %
                          (score_pixel_b, score_pixel_a))
                    score_pixel = score_pixel_b
                    # score_rms = self.RMS_Difference(image_a_XOR_b, image_b) / 1000
                    self.toggleDirection = False

            elif self.isDirectionSetH and self.toggleDirectionH:
                print("Running Horizontal Reverse XOR order!")
                score_pixel = score_pixel_a
                # score_rms = self.RMS_Difference(image_a_XOR_b, image_a) / 1000
            elif self.isDirectionSetH and not self.toggleDirectionH:
                print("Running Horizontal Standard XOR order!")
                score_pixel = score_pixel_b
                # score_rms = self.RMS_Difference(image_a_XOR_b, image_b) / 1000
            elif self.isDirectionSetV and self.toggleDirectionV:
                print("Running Vertical Reverse XOR order!")
                score_pixel = score_pixel_a
                # score_rms = self.RMS_Difference(image_a_XOR_b, image_a) / 1000
            elif self.isDirectionSetV and not self.toggleDirectionV:
                print("Running Vertical Standard XOR order!")
                score_pixel = score_pixel_b
                # score_rms = self.RMS_Difference(image_a_XOR_b, image_b) / 1000
            else:
                print("Something went wrong...")

        elif transformation == 'OR Images':
            image_a_OR_b = self.OR_images(image_a, image_b)
            list_a_OR_b = [self.RGB_to_Binary(
                pixel) for pixel in list(image_a_OR_b.getdata())]
            list_a = [self.RGB_to_Binary(pixel)
                      for pixel in list(image_a.getdata())]
            list_b = [self.RGB_to_Binary(pixel)
                      for pixel in list(image_b.getdata())]

            score_pixel_a = 100 * \
                len([i for i, j in zip(list_a_OR_b, list_a) if i == j]) / len(list_a)
            score_pixel_b = 100 * \
                len([i for i, j in zip(list_a_OR_b, list_b) if i == j]) / len(list_a)

            if not self.readyForSecondaryCompare:
                # if self.problem.name == 'Basic Problem B-10':
                #     image_a_OR_b.show()
                #     image_a.show()
                #     image_b.show()
                #     input()

                if score_pixel_a > score_pixel_b:
                    print("Reverse OR order works better! %f > %f" %
                          (score_pixel_a, score_pixel_b))
                    score_pixel = score_pixel_a
                    # score_rms = self.RMS_Difference(image_a_OR_b, image_a) / 1000
                    self.toggleDirection = True
                else:
                    print("Standard OR order works better! %f >= %f" %
                          (score_pixel_b, score_pixel_a))
                    score_pixel = score_pixel_b
                    # score_rms = self.RMS_Difference(image_a_OR_b, image_b) / 1000
                    self.toggleDirection = False

            elif self.isDirectionSetH and self.toggleDirectionH:
                print("Running Horizontal Reverse OR order!")
                score_pixel = score_pixel_a
                # score_rms = self.RMS_Difference(image_a_OR_b, image_a) / 1000
            elif self.isDirectionSetH and not self.toggleDirectionH:
                print("Running Horizontal Standard OR order!")
                score_pixel = score_pixel_b
                # score_rms = self.RMS_Difference(image_a_OR_b, image_b) / 1000
            elif self.isDirectionSetV and self.toggleDirectionV:
                print("Running Vertical Reverse OR order!")
                score_pixel = score_pixel_a
                # score_rms = self.RMS_Difference(image_a_OR_b, image_a) / 1000
            elif self.isDirectionSetV and not self.toggleDirectionV:
                print("Running Vertical Standard OR order!")
                score_pixel = score_pixel_b
                # score_rms = self.RMS_Difference(image_a_OR_b, image_b) / 1000
            else:
                print("Something went wrong...")

        elif transformation == 'AND Images':
            image_a_AND_b = self.AND_images(image_a, image_b)
            list_a_AND_b = [self.RGB_to_Binary(
                pixel) for pixel in list(image_a_AND_b.getdata())]
            list_a = [self.RGB_to_Binary(pixel)
                      for pixel in list(image_a.getdata())]
            list_b = [self.RGB_to_Binary(pixel)
                      for pixel in list(image_b.getdata())]

            score_pixel_a = 100 * \
                len([i for i, j in zip(list_a_AND_b, list_a) if i == j]) / len(list_a)
            score_pixel_b = 100 * \
                len([i for i, j in zip(list_a_AND_b, list_b) if i == j]) / len(list_a)
            if not self.readyForSecondaryCompare:
                # if self.problem.name == 'Basic Problem B-10':
                #     image_a_AND_b.show()
                #     image_a.show()
                #     image_b.show()
                #     input()

                if score_pixel_a > score_pixel_b:
                    print("Reverse AND order works better! %f > %f" %
                          (score_pixel_a, score_pixel_b))
                    score_pixel = score_pixel_a
                    # score_rms = self.RMS_Difference(image_a_AND_b, image_a) / 1000
                    self.toggleDirection = True
                else:
                    print("Standard AND order works better! %f > %f" %
                          (score_pixel_b, score_pixel_a))
                    score_pixel = score_pixel_b
                    # score_rms = self.RMS_Difference(image_a_AND_b, image_b) / 1000
                    self.toggleDirection = False

            elif self.isDirectionSetH and self.toggleDirectionH:
                print("Running Horizontal Reverse AND order!")
                score_pixel = score_pixel_a
                # score_rms = self.RMS_Difference(image_a_AND_b, image_a) / 1000
            elif self.isDirectionSetH and not self.toggleDirectionH:
                print("Running Horizontal Standard AND order!")
                score_pixel = score_pixel_b
                # score_rms = self.RMS_Difference(image_a_AND_b, image_b) / 1000
            elif self.isDirectionSetV and self.toggleDirectionV:
                print("Running Vertical Reverse AND order!")
                score_pixel = score_pixel_a
                # score_rms = self.RMS_Difference(image_a_AND_b, image_a) / 1000
            elif self.isDirectionSetV and not self.toggleDirectionV:
                print("Running Vertical Standard AND order!")
                score_pixel = score_pixel_b
                # score_rms = self.RMS_Difference(image_a_AND_b, image_b) / 1000
            else:
                print("Something went wrong...")
        elif transformation == 'Apply Difference':
            list_a = [self.RGB_to_Binary(pixel)
                      for pixel in list(image_a.getdata())]
            list_b = [self.RGB_to_Binary(pixel)
                      for pixel in list(image_b.getdata())]

            score_pixel = 100 * \
                len([i for i, j in zip(list_a, list_b) if i == j]) / len(list_a)
        else:
            list_a = [self.RGB_to_Binary(pixel) for pixel in list(
                image_a.transpose(transformation).getdata())]
            list_b = [self.RGB_to_Binary(pixel)
                      for pixel in list(image_b.getdata())]

            score_pixel = 100 * \
                len([i for i, j in zip(list_a, list_b) if i == j]) / len(list_a)
            # score_rms = self.RMS_Difference(image_a.transpose(transformation), image_b) / 1000

        score = score_pixel
        # score = (SCORE_PIXEL_WEIGHT * score_pixel) + (SCORE_RMS_WEIGHT * 100 - score_rms)
        print("Transformations Done: ", transformations_done, "Score: ", score)
        return score

    def PixelCompare_3x3(self, image_a, image_b, transformation):
        list_a = [self.RGB_to_Binary(pixel)
                  for pixel in list(image_a.getdata())]
        list_b = [self.RGB_to_Binary(pixel)
                  for pixel in list(image_b.getdata())]

        score_pixel = 100 * \
            len([i for i, j in zip(list_a, list_b) if i == j]) / len(list_a)
        return score_pixel
        # if transformation == 'AND Images':
        #     list_a = [self.RGB_to_Binary(pixel) for pixel in list(image_a.getdata())]
        #     list_b = [self.RGB_to_Binary(pixel) for pixel in list(image_b.getdata())]

        #     score_pixel = 100 * len([i for i, j in zip(list_a, list_b) if i == j]) / len(list_a)
        #     return score_pixel
        # elif transformation == 'OR Images':
        #     list_a = [self.RGB_to_Binary(pixel) for pixel in list(image_a.getdata())]
        #     list_b = [self.RGB_to_Binary(pixel) for pixel in list(image_b.getdata())]

        #     score_pixel = 100 * len([i for i, j in zip(list_a, list_b) if i == j]) / len(list_a)
        #     return score_pixel
        # elif transformation == 'XOR Images':
        #     list_a = [self.RGB_to_Binary(pixel) for pixel in list(image_a.getdata())]
        #     list_b = [self.RGB_to_Binary(pixel) for pixel in list(image_b.getdata())]

        #     score_pixel = 100 * len([i for i, j in zip(list_a, list_b) if i == j]) / len(list_a)
        #     return score_pixel
        # elif transformation == 'XOR Images':
        #     list_a = [self.RGB_to_Binary(pixel) for pixel in list(image_a.getdata())]
        #     list_b = [self.RGB_to_Binary(pixel) for pixel in list(image_b.getdata())]

        #     score_pixel = 100 * len([i for i, j in zip(list_a, list_b) if i == j]) / len(list_a)
        #     return score_pixel
        # return -1

    # Initialize the parameters relevant to each problem for easy access later
    def Initialize_Problem(self, problem):
        self.problem = problem
        self.is3x3 = self.problem.problemType == '3x3'

    # Print out a helpful heading to the console before each problem is being solved
    def Problem_Heading_Printer(self):
        print()
        print('***************************************************')
        print('Solving --', self.problem.name,
              ', which is --', self.problem.problemType)
        print('***************************************************')
        if ENV == 'dev':
            input()

    def Load_Problem_Images(self):
        try:
            image_a = self.Load_Image('A')
            image_b = self.Load_Image('B')
            image_c = self.Load_Image('C')

            if self.is3x3:
                image_d = self.Load_Image('D')
                image_e = self.Load_Image('E')
                image_f = self.Load_Image('F')
                image_g = self.Load_Image('G')
                image_h = self.Load_Image('H')
                return image_a, image_b, image_c, image_d, image_e, image_f, image_g, image_h
            else:
                return image_a, image_b, image_c
        except IOError as e:
            print('<IOError> Could not load problem images.')
            print(e)

    def Load_Problem_Answer_Images(self):
        try:
            image_1 = self.Load_Image('1')
            image_2 = self.Load_Image('2')
            image_3 = self.Load_Image('3')
            image_4 = self.Load_Image('4')
            image_5 = self.Load_Image('5')
            image_6 = self.Load_Image('6')

            if self.is3x3:
                image_7 = self.Load_Image('7')
                image_8 = self.Load_Image('8')
                return image_1, image_2, image_3, image_4, image_5, image_6, image_7, image_8
            else:
                return image_1, image_2, image_3, image_4, image_5, image_6
        except IOError as e:
            print('<IOError> Could not load problem answer images.')
            print(e)

    def Load_Image(self, key):
        image_name = self.problem.figures[key].visualFilename
        return Image.open(os.path.join(self.cd, image_name))

    def RGB_to_Binary(self, rgb_tuple):
        if rgb_tuple[0] + rgb_tuple[1] + rgb_tuple[2] < RGB_SUM:
            return 0  # black
        else:
            return 1  # white

    def AND_images(self, image_a, image_b):
        return ImageChops.add(image_a, image_b)

    def OR_images(self, image_a, image_b):
        return ImageChops.multiply(image_a, image_b)

    def XOR_images(self, image_a, image_b):
        image_diff = ImageChops.difference(image_a, image_b)
        return ImageChops.invert(image_diff)

    def Print_Time_Elapsed(self):
        time_elapsed = time.time() - self.time
        print('\nElapsed time was', int(time_elapsed * 1000), 'milliseconds.')

    def Print_Found_Match(self, answer):
        print('***************************************************')
        print('        ~`* SUCCESSFUL MATCH! Answer - %d *`~' % answer)
        print('***************************************************')
        if ENV == 'dev':
            input()

    def Print_No_Match(self):
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        print('                 ~`* NO MATCH *`~')
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

    def Rotate_Image(self, image, angle):
        return image.rotate(int(angle))
