"""
Relationship Advice Extraction Pipeline
This module extracts relationship advice content from free online sources.
All sources are free - no paid APIs required.

RETURNS:
1. List of Document objects containing:
   - page_content: The extracted text from each source
   - metadata: Dictionary with source URL, title, and other info

"""

import os
from typing import List, Dict, Any
from urllib.parse import urljoin

import bs4
from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader

# These are free websites with relationship advice content.
# Add or remove URLs based on your needs.

RELATIONSHIP_ADVICE_URLS = [
    # Reddit relationship advice (free, community-driven)
    "https://www.reddit.com/r/relationship_advice/",
    "https://www.reddit.com/r/dating_advice/",
    "https://www.reddit.com/r/relationships/",
    
    # WikiHow relationship articles (free, structured content)
    "https://www.wikihow.com/Category:Relationships",
    
    # Mind Body Green - free relationship articles
    "https://www.mindbodygreen.com/articles/relationships",
    
    # Psychology Today - free relationship content
    "https://www.psychologytoday.com/us/basics/relationships",
    
    # Healthline - free relationship advice
    "https://www.healthline.com/health/relationships",
    
    # Verywell Mind - free relationship content
    "https://www.verywellmind.com/love-and-relationships-4158229",
]

#Situationship queries for Sanjeevani and Me

SITUATIONSHIP_QUERIES = [
    "situationship advice",
    "undefined relationship signs",
    "how to define the relationship",
    "mixed signals in dating",
    "talking stage advice",
    "commitment issues modern dating",
    "emotional availability signs",
    "how to have the DTR talk",
]


def create_search_urls(query: str) -> List[str]:
    """
    Create search result URLs from free sources.
    
    Uses DuckDuckGo search results and
    other free search endpoints.
    
    Args:
        query: Search query string
        
    Returns:
        List of search result URLs
    """
    # DuckDuckGo HTML search
    duckduckgo_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}+relationship+advice"
    
    return [duckduckgo_url]


def extract_from_reddit(soup: bs4.BeautifulSoup, url: str) -> List[Dict[str, Any]]:
    """
    Extract relationship advice posts from Reddit.
    
    Args:
        soup: Parsed HTML content
        url: Source URL
        
    Returns:
        List of extracted content dictionaries
    """
    extracted = []
    
    # Find post containers
    posts = soup.find_all('div', class_='thing') or soup.find_all('article')
    
    for post in posts[:10]:  # Limit to 10 posts per source
        title_elem = post.find('a', class_='title') or post.find('h3')
        content_elem = post.find('div', class_='md') or post.find('p')
        
        if title_elem:
            title = title_elem.get_text(strip=True)
            content = content_elem.get_text(strip=True) if content_elem else ""
            
            if len(content) > 50:  # Filter out very short content
                extracted.append({
                    "title": title,
                    "content": f"{title}\n\n{content}",
                    "source": url,
                    "type": "reddit_post"
                })
    
    return extracted


def extract_from_generic_site(soup: bs4.BeautifulSoup, url: str) -> List[Dict[str, Any]]:
    """
    Extract content from generic article-based websites.
    
    Args:
        soup: Parsed HTML content
        url: Source URL
        
    Returns:
        List of extracted content dictionaries
    """
    extracted = []
    
    # Try to find article title
    title = ""
    title_tags = ['h1', 'h2', 'h3']
    for tag in title_tags:
        title_elem = soup.find(tag)
        if title_elem:
            title = title_elem.get_text(strip=True)
            break
    
    # Extract main content - try common article containers
    content_parts = []
    article_containers = [
        soup.find('article'),
        soup.find('div', class_='article-content'),
        soup.find('div', class_='post-content'),
        soup.find('div', class_='entry-content'),
        soup.find('main'),
    ]
    
    content_container = next((c for c in article_containers if c), soup)
    
    # Extract paragraphs
    paragraphs = content_container.find_all('p')
    for p in paragraphs[:20]:  # Limit paragraphs
        text = p.get_text(strip=True)
        if len(text) > 30:  # Filter short paragraphs
            content_parts.append(text)
    
    if content_parts:
        full_content = "\n\n".join(content_parts)
        extracted.append({
            "title": title or "Relationship Advice Article",
            "content": full_content,
            "source": url,
            "type": "article"
        })
    
    return extracted


def extract_from_search_results(soup: bs4.BeautifulSoup, query: str) -> List[Dict[str, Any]]:
    """
    Extract links and snippets from search engine results.
    
    Args:
        soup: Parsed HTML content
        query: Original search query
        
    Returns:
        List of extracted content dictionaries
    """
    extracted = []
    
    # DuckDuckGo result links
    results = soup.find_all('a', class_='result__url') or soup.find_all('a', class_='result__a')
    
    for result in results[:5]:  # Top 5 results
        link = result.get('href', '')
        title = result.get_text(strip=True)
        
        # Clean DuckDuckGo redirect URLs
        if 'uddg=' in link:
            link = link.split('uddg=')[1].split('&')[0]
        
        if link and link.startswith('http'):
            extracted.append({
                "title": title,
                "content": f"Search result for: {query}\nSource: {link}",
                "source": link,
                "type": "search_result"
            })
    
    return extracted


def load_web_content(urls: List[str]) -> List[Document]:
    """
    Load and parse content from web URLs using LangChain's WebBaseLoader.
    
    Args:
        urls: List of URLs to load
        
    Returns:
        List of LangChain Document objects
    """
    loader = WebBaseLoader(
        web_paths=urls,
        bs_kwargs={
            "parse_only": bs4.SoupStrainer(
                name=("article", "p", "h1", "h2", "h3", "div", "main")
            )
        },
        header_template={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
    )
    
    try:
        documents = loader.load()
        return documents
    except Exception as e:
        print(f"Error loading web content: {e}")
        return []


def extract_relationship_advice(
    use_predefined_urls: bool = True,
    use_search: bool = True,
    custom_urls: List[str] = None
) -> List[Document]:
    """
    Extracts relationship advice from free online sources.
    
    Args:
        use_predefined_urls: Whether to use the predefined list of relationship advice URLs
        use_search: Whether to perform additional searches for situationship content
        custom_urls: Optional list of custom URLs to scrape
        
    Returns:
        List of LangChain Document objects ready for ingestion
        
    DELIVERABLES:
    Each Document contains:
        - page_content: Extracted text content
        - metadata: {
            "source": URL of the source,
            "title": Article/post title,
            "type": Content type (article, reddit_post, search_result)
        }
    
    EXAMPLE OUTPUT:
    [
        Document(
            page_content="Signs you're in a situationship:\n1. No clear labels...",
            metadata={"source": "https://...", "title": "Situationship Signs", "type": "article"}
        ),
        ...
    ]
    """
    all_documents = []
    urls_to_scrape = []
    
    # Add predefined URLs
    if use_predefined_urls:
        urls_to_scrape.extend(RELATIONSHIP_ADVICE_URLS)
    
    # Add custom URLs
    if custom_urls:
        urls_to_scrape.extend(custom_urls)
    
    # Perform searches for situationship-specific content
    if use_search:
        for query in SITUATIONSHIP_QUERIES:
            search_urls = create_search_urls(query)
            # Extract search result links
            for search_url in search_urls:
                try:
                    search_docs = load_web_content([search_url])
                    for doc in search_docs:
                        # Parse search results to get actual article URLs
                        soup = bs4.BeautifulSoup(doc.page_content, 'html.parser')
                        search_results = extract_from_search_results(soup, query)
                        for result in search_results:
                            if result["source"] not in urls_to_scrape:
                                urls_to_scrape.append(result["source"])
                except Exception as e:
                    print(f"Search error for '{query}': {e}")
    
    # Remove duplicates and limit total URLs
    urls_to_scrape = list(dict.fromkeys(urls_to_scrape))[:50]
    
    print(f"Extracting content from {len(urls_to_scrape)} sources...")
    
    # Load content from all URLs
    documents = load_web_content(urls_to_scrape)
    all_documents.extend(documents)
    
    print(f"Successfully extracted {len(all_documents)} documents")
    
    return all_documents


def extract_from_specific_source(url: str) -> List[Document]:
    """
    Extract content from a single specific URL.
    
    Useful for targeted extraction from known high-quality sources.
    
    Args:
        url: Single URL to extract from
        
    Returns:
        List of Document objects from that source
    """
    print(f"Extracting from: {url}")
    documents = load_web_content([url])
    print(f"Extracted {len(documents)} documents")
    return documents


if __name__ == "__main__":
    pass
