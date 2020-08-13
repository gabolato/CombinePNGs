from PIL import Image
import numpy as np
import json
import os


def min_max_normalize(vals):
    min_val = min(vals)
    max_val = max(vals)
    return [(v - min_val) / (max_val - min_val) for v in vals]


def save_minimap(arr, width, name, suffix, output_path):
    m = np.array(arr).reshape((-1, width))
    res = Image.fromarray((m * 255).astype(np.uint8))
    res.save('{}/{}/{}_{}.bmp'.format(output_path, name, name, suffix), mode='w+')


def process(path, output_path, quad_size=128, aggregate_radius=128, x1=0, y1=0, x2=None, y2=None):
    arr = np.array(Image.open(path))
    px_height = arr.shape[0]
    px_width = arr.shape[1]
    print('(original): width: {}, height: {}, max:{} min:{}'.format(px_width, px_height, np.max(arr), np.min(arr)))

    # extract sub image
    x2 = px_width - x1 if not x2 else x2
    y2 = px_height - x2 if not y2 else y2
    arr = arr[y1: y1 + y2, x1: x1 + x2]

    px_height = arr.shape[0]
    px_width = arr.shape[1]
    print('(extracted): width: {}, height: {}, max:{} min:{}'.format(px_width, px_height, np.max(arr), np.min(arr)))

    means = []
    stds = []

    all_x = range(0, px_width - quad_size + 1, quad_size)
    all_y = range(0, px_height - quad_size + 1, quad_size)
    width = len(all_x)
    height = len(all_y)

    # aggregate stats
    for y in all_y:
        for x in all_x:
            sub_arr = arr[y: y + aggregate_radius, x:x + aggregate_radius]
            means.append(float(np.mean(sub_arr)))
            stds.append(float(np.std(sub_arr)))

    assert len(means) == width * height
    means = min_max_normalize(means)
    stds = min_max_normalize(stds)

    output_name = "{}x{}_size{}_radius{}_{}_{}".format(
        width,
        height,
        quad_size,
        aggregate_radius,
        os.path.split(path)[1].split('.')[0],
        '_'.join(map(str, [x1, y1, x1 + x2, y1 + y2]))
    )

    if not os.path.exists(output_path + '//' + output_name):
        os.makedirs(output_path + '//' + output_name)

    save_minimap(means, width, output_name, 'means', output_path)
    save_minimap(stds, width, output_name, 'stds', output_path)

    res = {'width': width, 'height': height, 'means': means, 'stds': stds}
    with open('{}/{}/{}.json'.format(output_path, output_name, output_name), 'w') as f:
        json.dump(res, f, indent=4)

    print(output_name)


# process('C://Users//sdq//geodata//elevation_5KMmd_GMTEDmd.tif', 'C://Users//sdq', 128, 128)
# 四川盆地
# process('C://Users//sdq//geodata//elevation_5KMmd_GMTEDmd.tif', 'C://Users//sdq', 4, 16, 6751, 1213, 6851, 1313)
# 喜马拉雅
# process('C://Users//sdq//geodata//elevation_5KMmd_GMTEDmd.tif', 'C://Users//sdq', 4, 16, 6304, 1291, 6404, 1391)
# 法国意大利
# process('C://Users//sdq//geodata//elevation_5KMmd_GMTEDmd.tif', 'C://Users//sdq', 2, 16, 4382, 865, 4582, 1065)
# 藏南
# process('C://Users//sdq//geodata//elevation_5KMmd_GMTEDmd.tif', 'C://Users//sdq', 4, 16, 6423, 1260, 300, 150)
# 西藏
# process('C://Users//sdq//geodata//elevation_5KMmd_GMTEDmd.tif', 'C://Users//sdq', 1, 16, 6543, 1277, 6643, 1377)
process('C://Users//sdq//geodata//elevation_5KMmd_GMTEDmd.tif', 'C://Users//sdq', 4, 16, 5997, 967, 856, 413)