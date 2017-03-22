#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import gensim
import codecs
from flask import Flask, render_template
from flask import request
from flask.json import jsonify
import json
from clarifai.client import ClarifaiApi
import os,sys,glob


app = Flask(__name__)

class DummyModel(object):

    """Um dummy só para ir mais rapido """

    def __getattr__(self, attr):
        def qualquer_coisa(*args, **kwargs):
            print args, kwargs
            return True
        return qualquer_coisa

model = DummyModel()

model = gensim.models.Word2Vec.load_word2vec_format("wiki.pt.trigram.vector", binary=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/operacoes', methods=['GET'])
def operacoes():
    return render_template('operacoes.html')

@app.route('/contexto', methods=['GET'])
def contexto():
    return render_template('contexto.html')

@app.route("/teste")
def hello():
    if request.args.get('most_similar'):

        print request.args.get('metric')

        if request.args.get('metric') == 'Wikipedia':
            similares = model_cgp.most_similar(request.args.get('most_similar'), topn=10)
        if request.args.get('metric') == 'Wikipedia':
            similares = model_cgj.most_similar(request.args.get('most_similar'), topn=10)
        if request.args.get('metric') == 'Wikipedia':
            similares = model.most_similar(request.args.get('most_similar'), topn=10)

        data_array = []

        number_nearest_words = len(similares)

        for j in range(0, number_nearest_words):
            data = {}
            data['name'] = similares[j][0]
            data['size'] = str(round(similares[j][1], 3))
            data['children'] = []
            print data
            print j
            data_array.append(data)
        print data_array
        
        json_data = json.dumps(data_array)
        print json_data

    	return jsonify({request.args.get('most_similar'): data_array})

    if request.args.get('context'):
        return jsonify({'context': model.doesnt_match(request.args.get('context').split())})


    if request.args.get('operation'):
        array_words = request.args.get('operation').split()
        print array_words

        if array_words[1] == '-':
            similares = model.most_similar(negative=[array_words[0], array_words[2]])
            data_array = []

            number_nearest_words = len(similares)

            print number_nearest_words

            for j in range(0, number_nearest_words):
                data = {}
                data['source'] = request.args.get('operation')
                data['target'] = similares[j][0]
                data['size'] = str(round(similares[j][1], 3))
                print data
                print j
                data_array.append(data)

            print data_array
        
            json_data = json.dumps(data_array)
            print json_data

            return jsonify({request.args.get('operation'): data_array})
        else:
            similares = model.most_similar(positive=[array_words[0], array_words[2]], negative=[array_words[4]])
            data_array = []

            number_nearest_words = len(similares)

            print number_nearest_words

            for j in range(0, number_nearest_words):
                data = {}
                data['source'] = request.args.get('operation')
                data['target'] = similares[j][0]
                data['size'] = str(round(similares[j][1], 3))
                print data
                print j
                data_array.append(data)
                # print data
            print data_array
        
            json_data = json.dumps(data_array)
            print json_data

            return jsonify({request.args.get('operation'): data_array})
        

    if request.args.get('graph'):
        similares = model.most_similar(request.args.get('graph'), topn=10)
        data_array = []

        if request.args.get('type') is "Global":
            pass

        number_nearest_words = len(similares)

        for j in range(0, number_nearest_words):
            data = {}
            data['source'] = request.args.get('graph')
            data['target'] = similares[j][0]
            data['size'] = str(round(similares[j][1], 3))
            print data
            print j
            data_array.append(data)
            # print data
        print data_array
        
        json_data = json.dumps(data_array)
        print json_data
        return json_data

    if request.args.get('mais_distante'):
    	return jsonify({'mais_distante': model.doesnt_match(request.args.get('mais_distante').split())})

if __name__ == "__main__":
    app.run()