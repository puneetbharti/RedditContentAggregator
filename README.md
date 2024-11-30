# RedditContentAggregator

A Python-based tool to aggregate trending content from multiple online sources like Reddit, RSS feeds, and Hacker News. This script fetches the top posts, extracts valuable comments, and filters them based on keywords of interest. The output is saved in an easy-to-read Excel format, making it ideal for content creators, researchers, and enthusiasts looking for daily trending topics in the fields of DevOps, AI, Blockchain, and Technology.

## Features

- Fetch top-ranking posts from specified subreddits.
- Extract top comments for deeper insights on each Reddit post.
- Aggregate content from popular RSS feeds such as TechCrunch and Hacker News.
- Save collected data into an Excel sheet for easy access.
- Filter topics based on keywords like `DevOps`, `Blockchain`, `AI`, and more.

## Prerequisites

To run this project, you'll need:

- Python 3.6+
- Reddit API credentials (client ID, client secret, user agent).

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/RedditContentAggregator.git
   cd RedditContentAggregator
   ```

2. **Install required packages:**
   
   Make sure you have `pip` installed and run:
   ```sh
   pip install -r requirements.txt
   ```

## Configuration

To use Reddit's API, you'll need to set up your API credentials.

- **Reddit API credentials:**
  - Register an application at [Reddit Apps](https://www.reddit.com/prefs/apps).
  - Fill in your `client ID`, `client secret`, and `user agent` in the script (`REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT`).

## Running the Script

To run the script and collect the latest top posts, use:
```sh
python reddit_content_aggregator.py
```

The script will generate an Excel file (`daily_content_<date>.xlsx`) in the `output` folder, containing:

- **Title** of the post.
- **URL** to the content.
- **Source** of the content (subreddit or other news site).
- **Type** (Article or Meme).
- **Score** (the number of upvotes on Reddit).
- **Top Comments** (top 3 comments for each post).

## Usage

- **Content Creators**: Quickly find daily trending tech topics to create engaging content.
- **Researchers**: Keep track of what's being discussed in the tech world.
- **Enthusiasts**: Stay informed about the latest in DevOps, AI, and blockchain.

## Contributions

Contributions are welcome! If you have ideas for improving the script or adding more features, please feel free to open an issue or submit a pull request.

1. **Fork the repository**
2. **Create a new feature branch**
   ```sh
   git checkout -b feature/your-feature
   ```
3. **Commit your changes**
   ```sh
   git commit -m "Add your feature"
   ```
4. **Push to the branch**
   ```sh
   git push origin feature/your-feature
   ```
5. **Open a pull request**

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

## Acknowledgements

- Built using [PRAW](https://praw.readthedocs.io/) for Reddit integration.
- RSS parsing via [feedparser](https://pythonhosted.org/feedparser/).
- Inspiration from daily content aggregators and tech enthusiasts.


