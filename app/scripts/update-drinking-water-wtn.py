# update_wells.py

import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gwells.settings")
django.setup()

from wells.models import Well

def main():
    well_tag_numbers = [
        2, 52, 74, 194, 195, 222, 224, 251, 702, 757, 763, 777, 778, 1024, 1119,
        1120, 1123, 1124, 1125, 1126, 1133, 1135, 1137, 1141, 1142, 1146, 1166,
        1173, 1175, 1180, 1190, 1192, 1198, 1201, 1212, 1213, 1230, 2210, 2396,
        4983, 5684, 7907, 8884, 9870, 13446, 13884, 14048, 14259, 15036, 15492,
        15971, 16002, 16245, 16573, 17629, 17922, 18056, 18149, 18598,
        18610, 18822, 19096, 19226, 19331, 19380, 19905, 20074, 20076, 
        20422, 20497, 20502, 20711, 20734, 20834, 20846, 20930, 21027,
        21038, 21066, 21099, 21120, 21171, 21189, 21214, 21324, 21432,
        21463, 21476, 21488, 21599, 21600, 21690, 21751, 21867, 21873,
        21899, 22181, 22427, 23140, 23203, 23204, 23205, 23253, 23310,
        23423, 23494, 24472, 24603, 24631, 24811, 25255, 25477, 25834,
        25837, 25896, 25897, 25909, 26810, 27459, 27470, 27493, 27795,
        28613, 29287, 29541, 29542, 29688, 29692, 30128, 31070, 31464,
        31486, 31631, 31816, 31817, 31818, 32143, 32497, 33538, 33596,
        34031, 34049, 34154, 34272, 34496, 34506, 34572, 34654, 35012,
        35232, 35354, 35486, 35487, 35546, 36228, 36299, 36302, 36304,
        36524, 36528, 36529, 36530, 36531, 36547, 36666, 37325, 37531,
        38650, 38724, 38872, 38874, 39123, 40027, 40308, 40631, 40931,
        41982, 42201, 42268, 43695, 43810, 43922, 44030, 44236, 44238,
        44241, 44243, 44358, 44725, 44868, 45622, 45683, 47039, 47818,
        47826, 48237, 48639, 48678, 49169, 49481, 49619, 49649, 49839,
        49840, 49841, 51335, 51386, 51419, 51507, 51572, 52088, 52120,
        52594, 52925, 52952, 52963, 53533, 53615, 53718, 54004, 54069,
        54090, 54190, 54317, 54422, 54467, 54723, 55800, 55890, 56319,
        56349, 56804, 56805, 56806, 56808, 56888, 56910, 56930, 57074,
        57099, 57315, 57771, 57828, 57836, 57993, 58008, 58096, 58601,
        58620, 58625, 58638, 58671, 58733, 58745, 58768, 58910, 59137,
        59208, 59227, 59336, 59589, 59590, 59633, 59745, 59849, 59926,
        59927, 59928, 59930, 59965, 60165, 62250, 62251, 62941, 68619,
        69141, 69537, 71593, 74681, 75317, 75318, 77913, 80585, 80587,
        80588, 80590, 80591, 80592, 81674, 82339, 82340, 82341, 82377,
        82378, 82382, 82395, 82665, 82957, 83008, 83125, 83180, 83181,
        84003, 84682, 84718, 84720, 85154, 85155, 85156, 85207, 85208,
        85209, 85725, 86644, 86645, 93746, 93749, 93750, 93902, 93903,
        93905, 93906, 93907, 94063, 94065, 94096, 94097, 94199, 98194,
        98197, 98330, 98537, 98858, 99544, 102257, 102267, 102272, 102273,
        102274, 102370, 102383, 102384, 102385, 102386, 102387, 102388,
        102389, 102392, 102394, 102398, 102399, 102400, 102401, 102402,
        102404, 102405, 102406, 102407, 102408, 102409, 102410, 102412,
        102413, 102414, 102418, 102421, 102424, 102441, 102442, 102443,
        102444, 102445, 102446, 102451, 102452, 102482, 102487, 102488,
        102490, 102500, 102542, 102558, 102666, 102842, 103038, 104350,
        104404, 104412, 104422, 104693, 104694, 105351, 105352, 105353,
        105355, 105357, 105358, 105359, 105360, 105361, 105441, 105451,
        105453, 105622, 105643, 105645, 105647, 105648, 105649, 105650,
        105651, 105652, 105653, 105738, 105739, 105740, 105742, 105743,
        105744, 106345, 107476, 111370, 111371, 119363, 119366]

    for tag_number in well_tag_numbers:
        try:
            well = Well.objects.get(well_tag_number=tag_number)
            well.drinking_water_protection_area_ind = True
            well.save()
            print(f"Well with tag number {tag_number} updated successfully.")
        except Well.DoesNotExist:
            print(f"Well with tag number {tag_number} not found.")

if __name__ == "__main__":
    main()
