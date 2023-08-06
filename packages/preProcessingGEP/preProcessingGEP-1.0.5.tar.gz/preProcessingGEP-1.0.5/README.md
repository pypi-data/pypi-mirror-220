## Usage of PreProcessingService

You can access following functions:

The provided package is a collection of functions for text preprocessing and cleaning. Here is a brief explanation of each function:

_en_stopwords: Returns a list of English stopwords.

strip_numeric: Removes numbers from a string.

strip_punctuation: Removes all punctuation marks from a string.

remove_stopwords: Removes stopwords from a string.

strip_multiple_whitespaces: Removes excess whitespace from a string.

strip_short: Removes words with a length less than a specified size from a string.

remove_alpha_num: Removes alphanumeric characters from a string.

lemmatize: Lemmatizes a list of tokens.

nltk_pos: Performs Part-of-Speech (POS) tagging using NLTK.

stanford_pos: Performs POS tagging using Stanford POS Tagger.

filter_pos: Filters words based on specific POS tags.

clean_text: Cleans the text by applying various cleaning functions.

preprocess_string: Preprocesses a string by applying a list of cleaning functions.

preprocess_postags: Applies a list of filtering functions to a list of strings.

guided_buy_preprocess: Preprocesses a list of strings for guided buying purposes.

dump_interim_steps: Creates a DataFrame with the intermediate steps of preprocessing.

lemmatization: Performs lemmatization on a string.

cold_start_preprocess: Preprocesses a list of words for cold start purposes.

unique_value_col: Splits words based on '|'.

convert_synonyms:A collection of synonym mappings

clean_description: Includes all above cleaning steps

## Example usage: 
>> pip install preProcessingGEP==1.0.4

import preProcessingGEP

print(preProcessingGEP.PreProcessingService.clean_description(inputText))

### General Syntax to use any function
#### preProcessingGEP.PreProcessingService.function_name()