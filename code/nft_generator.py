import os
import sys

from config import NFT_CSV, SCRIPT_PATH

sys.path.append(SCRIPT_PATH)
import json
import numpy as np
import pandas as pd


class NftGen:
    def __init__(self) -> None:
        self._content = {}
        self._parser = NftParser()
        self._set_seed()
        self._load()

    def check(self, model, ind):
        # returns the name of the relevant nft if this index has one.
        # otherwise returns none
        nfts = [key for key, x in self._content[model.lower()].items() if ind in x]
        if len(nfts)>0:
            print("NFTs", nfts)
            return nfts[0]
        #path="C:/Users/STFED/_A/_other/PantiesPorn_1/assets/Master_Generator/Material_Library/NFT"
        #nft = np.random.choice([x for x in os.listdir(path) if not os.path.isdir(f'{path}/{x}')], 1)[0]
        #print("NFT:", nft)
        #return nft


    def _load_json(self):
        return json.load(open("code/models.json"))

    def _load(self):

        """
        Erykah: {NFT1 : [123, 154]}
        """
        _jsonfile = self._load_json()
        _amounts = self._produce_amount(_jsonfile)
        for amount, (model, params) in zip(_amounts, _jsonfile.items()):
            self._produce(model, params, amount)

    def _produce_amount(self, _jsonfile):
        nft_models = np.array([x[1] for x in _jsonfile.values()])
        _temp = np.random.rand(nft_models.sum())
        _temp = _temp / _temp.sum()
        nft_models[np.nonzero(nft_models)[0]] = _temp * self._parser.get_total()
        nft_models = nft_models.astype(np.uint8)
        diff = self._parser.get_total() - nft_models.sum()
        if diff > 0:
            nft_models[-1] += diff
            
        return nft_models.astype(np.uint8)

    def _produce(self, model, params, amount):
        self._content[model] = {}
        if params[1] == 1:
            # names of nfts we create
            nfts = np.random.choice(self._parser.get_remaining(), amount, replace=False)
            print(params[0], amount)
            numbers = np.random.choice(range(1, params[0]), amount, replace=False)
            
            for nft, number in zip(nfts, numbers):
                if nft not in self._content[model]:
                    self._content[model][nft] = []
                self._content[model][nft].append(number)
                self._parser.exclude(nft, 1)

    def _set_seed(self):
        np.random.seed(117)



class NftParser:
    def __init__(self) -> None:
        
        self._id_col = "File name"
        self._total_col = "total"
        
        self._content = self._load()
        self._dict = {"filename": self._id_col,
                      "tag":"Upcycled NFT",
                      "author": self._content.columns[4],
                      "quantity": "Quantity"
        }
        self._update()

    def exclude(self, name, quantity):
        ind = self._content.loc[self._content[self._id_col]==name][self._dict["quantity"]].index[0]
        self._content.at[ind, self._dict["quantity"]] = max(0, self._content.at[ind, self._dict["quantity"]] - quantity)
        if self._content.at[ind, self._dict["quantity"]] == 0:
            self._content.drop(ind, axis=0, inplace=True)
        self._update()

    def get(self, filename, key):
        return self._get(filename, key)

    def get_remaining(self):
        return self._content[self._total_col].sum()

    def get_total(self):
        return self._content[self._dict["quantity"]].sum()

    def _get(self, filename, key):
        if "." in filename:
            filename = "".join(filename.split(".")[:-1])
            
        if key.lower() in self._dict.keys():
            try:
                return self._content.loc[self._content[self._id_col]==filename][self._dict[key]].iloc[0]
            except Exception as e:
                print(repr(e))
                print(filename)
                print(self._content.loc[self._content[self._id_col]==filename][self._dict[key]])

    def _load(self):
        return pd.read_csv(NFT_CSV)
        

    def _update(self):
        self._content[self._total_col] = [[x] for x in self._content[self._id_col]]
        self._content[self._dict["quantity"]].fillna(value=0, inplace=True)
        self._content[self._total_col] = self._content[self._total_col] * self._content[self._dict["quantity"]].astype(int)
