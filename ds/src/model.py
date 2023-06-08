import numpy as np
import pandas as pd
import json
import pickle


def predict(d):
    answer = dict()
    answer['orderkey'] = d['orderId']
    cnt = 0
    all_packs = ['YMA', 'YMC', 'YME', 'YMF', 'YMG', 'YML', 'YMU', 'YMV',
                 'YMW', 'MYF', 'YMX', 'MYA', 'MYB', 'MYC', 'MYD', 'MYE']
    for item in d['items']:
        cnt += item['count']
    if cnt > 5:
        answer['status'] = 'fallback'
        return answer

    elif cnt == 1:
        with open('sku_pack_dict.json') as f:
            sku_pack_dict = json.load(f)
        if d['items'][0]['type'][0] == '340':
            answer['package'] = [{'cartontype': 'NONPACK', 'goods': [d['items'][0]['sku']]}]
            answer['status'] = 'ok'
            return answer

        elif d['items'][0]['type'][0] == '360':
            answer['package'] = [{'cartontype': 'STRETCH', 'goods': [d['items'][0]['sku']]}]
            answer['status'] = 'ok'
            return answer

        elif d['items'][0]['sku'] in sku_pack_dict:
            answer['package'] = [{'cartontype': sku_pack_dict[d['items'][0]['sku']], 'goods': [d['items'][0]['sku']]}]
            answer['status'] = 'ok'
            return answer

        else:
            carton_edited = pd.read_csv('carton_edited.csv')
            valid_pack = []
            for pack in all_packs:
                if (np.min([float(d['items'][0]['size1']), float(d['items'][0]['size2']), float(d['items'][0]['size2'])]) < np.min(carton_edited.loc[carton_edited['CARTONTYPE'] == pack,['LENGTH', 'WIDTH', 'HEIGHT']].values)
                    and np.max([float(d['items'][0]['size1']), float(d['items'][0]['size2']), float(d['items'][0]['size2'])]) < np.max(carton_edited.loc[carton_edited['CARTONTYPE'] == pack,['LENGTH', 'WIDTH', 'HEIGHT']].values)
                    and np.median([float(d['items'][0]['size1']), float(d['items'][0]['size2']), float(d['items'][0]['size2'])]) < np.median(carton_edited.loc[carton_edited['CARTONTYPE'] == pack,['LENGTH', 'WIDTH', 'HEIGHT']].values)
                    ):
                    valid_pack.append(pack)
            if len(pack) == 0:
                answer['status'] = 'fallback'
                return answer

            pack_to_return = (carton_edited.loc[carton_edited['CARTONTYPE'].isin(all_packs), ['CARTONTYPE', 'price']]
                                            .sort_values('price')['CARTONTYPE']
                                            .tolist()[0])
            answer['package'] = [{'cartontype': pack_to_return, 'goods': [d['items'][0]['sku']]}]
            answer['status'] = 'ok'
            return answer

    else:
        result = []
        for item in d['items']:
            count = item['count']
            size1 = float(item['size1'])
            size2 = float(item['size2'])
            size3 = float(item['size3'])
            weight = float(item['weight'])
            volume = size1 * size2 * size3
            result.extend([size1, size2, size3, volume, weight] * count)
        if len(result) < 25:
            result.extend([0] * (25-len(result)))
        with open('model.pcl', 'rb') as fid:
            model = pickle.load(fid)

        probs = model.predict_proba(np.array(result).reshape(1, -1))[0]
        ind = np.argsort(probs)[::-1][:3]
        l = []
        for p in model.classes_[ind]:
            l.append({'cartontype': p, 'goods': [x['sku'] for x in d['items']]})
        answer['package'] = l
        answer['status'] = 'ok'
        return answer
