# Enigma-Machine-Libary

This library provides functions for simulating the Enigma Machine, a historical encryption device used during World War II. The library was created as part of an assessment for INSPER college in São Paulo, Brazil.

Functions
The library includes the following functions:

The following functions are part of an encryption/decryption system based on an enigma machine.

----------------------------------------------------------------

`to_one_hot`

Converts a string of letters into a matrix representation using one-hot encoding.

Args:
message: str containing the letters to be encoded.

Returns:
np.ndarray: matrix with one-hot encoding of the input message.

----------------------------------------------------------------

`to_string`

Converts a matrix of one-hot encoded characters into a string of letters.

Args:
matrix: np.ndarray containing the one-hot encoded characters.

Returns:
str: string of letters corresponding to the input matrix.


----------------------------------------------------------------

`encrypt`
Encrypts a message using a permutation matrix.

Args:
message: str containing the message to be encrypted.
permutation_matrix: np.ndarray representing the permutation matrix to be used for encryption.

Returns:
str: encrypted message

----------------------------------------------------------------

`decrypt`

Decrypts an encrypted message using a permutation matrix.

Args:
encrypted_message: str containing the message to be decrypted.
permutation_matrix: np.ndarray representing the permutation matrix to be used for decryption.

Returns:
str: decrypted message.

----------------------------------------------------------------

`enigma_machine`

Encrypts a message using a permutation matrix and an auxiliary matrix.

Args:
message: str containing the message to be encrypted.
permutation_matrix: np.ndarray representing the permutation matrix to be used for encryption.
auxiliary_matrix: np.ndarray representing the auxiliary matrix to be used for encryption.

Returns:
str: encrypted message.

----------------------------------------------------------------

`enigma_machine_decrypt`

Decrypts an encrypted message using a permutation matrix and an auxiliary matrix.

Args:
encrypted_message: str containing the message to be decrypted.
permutation_matrix: np.ndarray representing the permutation matrix to be used for decryption.
auxiliary_matrix: np.ndarray representing the auxiliary matrix to be used for decryption.

Returns:
str: decrypted message.
