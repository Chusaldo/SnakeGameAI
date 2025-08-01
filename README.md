# 🐍 Snake Game + NEAT AI

This project includes two versions of the classic **Snake** game:

* 🎮 `snake.py`: human-playable version with keyboard controls.
* 🤖 `snakeAI.py`: automated version where a neural network learns to play using **NEAT (NeuroEvolution of Augmenting Topologies)**.

---

## 📂 Project Structure

```
📁 Snake/
├───AI
│    ├─── snakeAI.py    # Snake game controlled by neural network (AI)
     └─── config.txt    # NEAT algorithm configuration
├───Graphics            # Graphics assets (e.g., food image)
      └─── food.png
├───Normal
      └─── snake.py     # Classic Snake game (human-controlled)
└───Sounds              # Sound effects (eat and crash)
      ├─── eat.mp3
      └─── wall.mp3              
```

---

## 🎮 snake.py – Human Mode

Classic Snake game built with Pygame:

* Use arrow keys to move the snake
* Earn points by eating food
* Lose if you hit a wall or yourself

```bash
python snake.py
```

---

## 🤖 snakeAI.py – AI Mode (NEAT)

The AI trains a neural network to play Snake automatically using the **NEAT** algorithm:

```bash
python snakeAI.py
```

### Features:

* Training with multiple snakes in parallel
* Real-time visualization of training process
* Neural network is trained with 10 inputs:

  * Danger ahead, left, right
  * Food direction relative to snake
  * Current direction (one-hot encoded)
---

## ⚙️ NEAT Configuration

The `config.txt` file defines evolutionary parameters:

* Input nodes: 10
* Output nodes: 3 (left, straight, right)
* Population size: 100
* Mutation rates, elitism, speciation, etc.

Feel free to tune this file to experiment with different architectures.

---

## 📌 Requirements

* Python 3.8+
* Pygame
* NEAT-Python

```bash
pip install pygame neat-python
```

---

## ✍️ Author

Developed by **Jesús González Díaz**
Inspired by biological evolution (NEAT) and [Nick Koumaris](https://github.com/educ8s/Python-Retro-Snake-Game-Pygame).

---

## 🧪 Future Ideas

* Add "extended vision" or full-map awareness
* Train in headless mode (no Pygame)
* Save/load entire populations
* Live training stats dashboard
