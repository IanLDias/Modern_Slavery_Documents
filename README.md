# About

Largely inspired by the work done by The Future Society, available at https://github.com/the-future-society/modern-slavery-statements-research.

The UK Modern Slavery Act (MSA) requires companies above a certain valuation to report steps that they are taking to to abolish modern slavery from their operations. 

Australia has now also implemented a similar act. 

This consists of thousands of PDFs every year submitted by these companies.


# Goals

The goal of this project is to implement an information extraction framework for these PDFs

1) Text Summarization of the PDFs 
    - Extractive Approach: identifying key sentences and phrases and using these in a summary
    - Abstractive Approach: Generating a summary (WIP)
2) Relevance Score
    - Calculates the TF-IDF of each document and compares document similarities
    - Makes a list of the most and least relevant document. Found in TF-IDF sklearn.ipynb
3) Identifying companies at risk
    - Testing knowledge graphs for information extraction and linkage (6th April)