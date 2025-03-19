# README

This repository contains our implementation of **VQ-VAE + Genetic Algorithm for Level Blending**, which builds on the ideas presented in our paper. Below is an overview of how each part of the code maps to our methodology and where you can find the relevant functions.

---

## 1. Data Preparation and One-Hot Encoding

We start by preparing 16×16 chunks from Super Mario Bros. (SMB) and Kid Icarus (KI) levels. These chunks are drawn from the [Video Game Level Corpus (VGLC)](https://github.com/TheVGLC/TheVGLC). The code for these steps is in:

- **`get_smb_data()`** and **`get_ki_data()`**  
  - Reads `.txt` files for each game map, converts them into 2D arrays using `text_2_mat()`, and slices them into **16×16** chunks (`get_chunks()`).
  - One-hot encodes each tile with `one_hot()` so we can feed the data into our neural network.

- **`replacement_table`** and **`replacement_table_inverse`**  
  - Provide a mapping between characters (tiles) and their one-hot vector representations (and vice versa).

These steps implement the data processing we described in the paper, ensuring the game levels are fully prepared for training.

---

## 2. VQ-VAE Architecture

We use a **Vector-Quantized Variational Autoencoder (VQ-VAE)** to learn a discrete latent space from the SMB + KI data:

- **`VectorQuantizer` class**  
  - Implements our discrete codebook.  
  - The `call()` method quantizes encoder outputs by mapping them to their nearest embedding vectors.  
  - The `get_code_indices()` method computes these nearest-embedding lookups.

- **`get_encoder(latent_dim=16)`**  
  - Builds a convolutional encoder that reduces each 16×16×18 input chunk down to a 4×4×`latent_dim` feature map.

- **`get_decoder(latent_dim=16)`**  
  - Uses upsampling and transposed convolutions to reconstruct the original 16×16×18 shape.

- **`get_vqvae(latent_dim=16, num_embeddings=64)`**  
  - Combines the encoder, `VectorQuantizer`, and decoder into a single Keras Model.

This section covers the core of our VQ-VAE approach from the paper, where we capture a **discrete latent space** that represents both SMB and KI levels.

---

## 3. VQ-VAE Training Procedure

- **`VQVAETrainer` class**  
  - Wraps the training logic into a Keras `Model`.
  - The `train_step()` method calculates:
    1. **Reconstruction loss** (comparing input chunks to their reconstructions),  
    2. **Vector-Quantization loss** (commitment and codebook terms),  
    3. Applies gradients via the usual Keras flow.

This aligns with how we trained the VQ-VAE in our paper, optimizing both reconstruction quality and proper embedding usage in the discrete latent space.

---

## 4. Genetic Algorithm (GA) for Level Blending

To introduce further creativity and control over blending proportions, we apply a Genetic Algorithm. This step can operate directly on tile-level chunks or in the latent space produced by the VQ-VAE:

- **`mutation(individual, mutation_rate)`**  
  - Randomly changes one tile (or latent element) to another tile/embedding based on a specified probability.

- **`crossover(individual_1, individual_2, crossover_rate)`**  
  - Selects columns (or rows) from two parent chunks to create two children.

- **`fitness(individual, passable_point, ...)`**  
  - Evaluates how “blended” a chunk is by comparing the proportion of passable vs. solid tiles with our desired distribution.  
  - Implements the paper’s idea of a *blending point* between SMB and KI.

- **`evolution(...)`**, **`generation(...)`**, **`main()`**  
  - Encompass selection, maintaining population limits, and iteratively applying crossover + mutation.  
  - `main()` shows an example loop running multiple generations, then saves the best results.

In our paper, we highlight how using GA in the **latent space** of the VQ-VAE helps steer the generation of hybrid levels while preserving realistic structures learned from both games.

---

## 5. Visualization

We provide methods to view and compare chunk outputs:

- **`visualize_ga(chunk)`**  
  - Renders a 2D chunk as a sprite-based image.  
- **`print_side_by_side(chunk_1, chunk_2)`**  
  - Prints two chunks (e.g., original vs. reconstructed) side by side for comparison.  
- Other similar helpers (`visualize()`, etc.) let us inspect the generated or blended levels visually, matching the figures we reference in our paper.

---

## Key Highlights

1. **Data Loading** (`get_smb_data()`, `get_ki_data()`) → Create **16×16** one-hot chunks for SMB & KI.  
2. **VQ-VAE** (`get_vqvae()`, `VectorQuantizer`, `VQVAETrainer`) → Discrete latent space capturing features from both games.  
3. **GA** (`mutation()`, `crossover()`, `fitness()`, `generation()`) → Searches level or latent space, guided by blending constraints.  
4. **Visualization** → Demonstrates and verifies the **blended levels**.

This matches the methodology we presented: we first train a VQ-VAE to learn a unified latent space for both games, and then use an evolutionary search to produce levels that lie anywhere between the SMB and KI style distributions. 

We hope you find this code helpful for understanding or reproducing our experiments on **Level Blending with a Genetic Algorithm in the VQ-VAE Latent Space**!
