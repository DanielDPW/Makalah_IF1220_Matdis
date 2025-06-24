# IF1220 - Discrete Mathematics

<a href="https://github.com/DanielDPW/Makalah_IF1220_Matdis/tree/main/docs"><strong>Documentation »</strong></a>
<br />
</p>

This repository contains an implementation made in Python for modelling relationship dynamics using weighted graph in the Iterated Prisoner's Dilemma.

<br/>
<br/>
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#project-structure">Project Structure</a>
    </li>
    <li>
      <a href="#how-to-use">How To Use</a>
    </li>
  </ol>
</details>
<br/>

## About The Project

This project explores the usage of graph theory, and specifically weighted graphs to model relationship dynamics between multiple players in the Iterated Prisoner's Dilemma. The core principle uses weighted graph to represent the strength of the relation between two players. Defection causes this relationship to strain and when the relationship reaches a certain thresholds, it severs and both players no longer interact. This gives a more accurate way of mimicking real world relationship by allowing the players to cut ties with players that are bad actors.



## Project Structure
```ssh
.
├── README.MD
├── docs
│   └── Weighted Graph-Based Modelling of Relationship Dynamics to Determine Optimal Strategies for Long-Term Payoffs in the Iterated Prisoner’s Dilemma.pdf
└── src
    └── matdis.py
```

## How To Use

1. Make sure the dependencies are installed (Python, Axelrod, Networkx, Matplotlib)

2. Clone the repository
    ```sh
    git clone https://github.com/DanielDPW/Makalah_IF1220_Matdis.git
    ```

3. Change to repository's directory
    ```sh
    cd Makalah_IF1220_Matdis
    ```

4. Adjust the simulation parameters.

5. Run the program
    ```sh
    cd src
    python matdis.py
    ```

