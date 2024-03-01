## Delete Reddit Comments

This project aims to provide a solution for deleting Reddit comments in bulk. You can use the batch_size to change the amount of comments you preview before you delete. If you choose to not delete a set of commments, you get the choice to go through that batch and delete comments individually.

### Prerequisites

Before running the script, make sure you have the following prerequisites installed:

- Python 3.x
- PRAW (Python Reddit API Wrapper)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/Delete-Reddit-Comments.git
    ```

2. Install the required dependencies:

    ```bash
    pip install praw
    ```

### Usage

1. Update the `sample.env` file with your Reddit API credentials.

2. Run the script:

    ```bash
    python delete_comments.py
    ```

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.