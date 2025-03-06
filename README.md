# FairPlay: Using Generative AI to Forge Fairer Societal Agreements

## Project Overview
FairPlay is a capstone project that leverages generative AI to simulate bilateral negotiations with the aim of promoting fairness in societal agreements. Inspired by John Rawls' Theory of Justice, this project explores how AI can help identify and address biases in agreements, such as employment contracts, service agreements, and lease agreements.

The project focuses on simulating negotiations between AI agents, incorporating cognitive, emotional, and strategic elements to understand fairness dynamics. By implementing principles from Rawls' "veil of ignorance" and Pareto efficiency, FairPlay aims to create AI-driven tools that can guide real-world contract negotiations towards more equitable outcomes.

## Methodology
1. **Simulated Multi-agent Setting**: AI agents start negotiations behind a "digital veil of ignorance," unaware of the social status or preferences of the entities they represent.
2. **Iterative Renegotiation**: Agents continually renegotiate agreements, evaluating terms until fairness is reached.
3. **Agreement Analysis**: A system to assess biases and quantify the fairness of contracts based on initial and final terms.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/aegerita/FairPlay.git
    ```
2. Navigate to the project directory:
    ```bash
    cd FairPlay
    ```
3. Install the necessary dependencies:
    ```bash
    poetry install
    ```
4. Create a `.env` file in the root directory based on the `.env.example` file.

## Usage
Run the simulation by executing the simulation scripts. For example:
```bash
python ./src/fairplay/main.py --folder_path 'src/docs/SC vs TC/'
```
This will initialize the AI agents and begin the negotiation simulation. 

## Results and Insights
FairPlay generates reports that detail the negotiation process, the fairness of the outcomes, and key metrics. These reports will help in understanding the impact of different negotiation strategies and fairness principles.

## Future Development
- **Integration of More Complex Contracts**: Expand the scope of contracts to include more real-world legal documents.
- **Agent Emotion Modeling**: Enhance emotional modeling to better reflect human negotiation patterns. ### Why is this benefitial? ###
- **User Interface**: Build a user-friendly interface for non-technical users to interact with the simulation.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For inquiries or contributions, feel free to reach out to me or via the repository's Issues page.
