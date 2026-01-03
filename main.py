import argparse
import json
from article_generator import ArticleGenerator
from config import config


def main():
    parser = argparse.ArgumentParser(description="Article Generator using LangChain and Ollama")
    parser.add_argument("--topic", type=str, help="Topic for the article")
    parser.add_argument("--tone", type=str, default="professional",
                        choices=["professional", "conversational", "persuasive", "educational", "entertaining"])
    parser.add_argument("--length", type=int, default=800, help="Target article length in words")
    parser.add_argument("--keywords", type=str, default="", help="Keywords to include (comma-separated)")
    parser.add_argument("--style", type=str, default="informative",
                        choices=["informative", "persuasive", "narrative", "descriptive"])
    parser.add_argument("--research", type=str, help="Path to research materials file (text or JSON)")
    parser.add_argument("--enhance", action="store_true", help="Enhance existing article")
    parser.add_argument("--variants", type=int, default=0, help="Generate multiple variants")
    parser.add_argument("--output", type=str, help="Output file path")

    args = parser.parse_args()

    print("Initializing Article Generator...")
    generator = ArticleGenerator()

    # ----------------------------------------

    if args.enhance and args.topic:
        article = generator.create_article_from_scratch(
            topic=args.topic,
            tone=args.tone,
            length=args.length,
            keywords=args.keywords,
            style=args.style
        )

        enhanced = generator.enhance_existing_article(article)

        print("\n" + "=" * 50)
        print("ENHANCED ARTICLE")
        print("=" * 50)
        print(enhanced)

        if args.output:
            generator.save_article(enhanced, args.output)

    # ----------------------------------------

    elif args.variants > 0 and args.topic:
        variants = generator.generate_multiple_variants(args.topic, args.variants)

        for i, variant in enumerate(variants):
            print("\n" + "=" * 50)
            print(f"VARIANT {i + 1} - {variant['tone'].upper()} TONE")
            print("=" * 50)
            print(variant["content"])

            if args.output:
                filename = args.output.replace(".txt", f"_variant_{i + 1}.txt")
                generator.save_article(variant["content"], filename)

    # ----------------------------------------

    elif args.research and args.topic:
        research_materials = []

        if args.research.endswith(".json"):
            with open(args.research, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    research_materials = data
                else:
                    research_materials = [json.dumps(data)]
        else:
            with open(args.research, "r", encoding="utf-8") as f:
                research_materials = [f.read()]

        article = generator.generate_with_research(args.topic, research_materials, args.tone)

        print("\n" + "=" * 50)
        print("RESEARCH-BASED ARTICLE")
        print("=" * 50)
        print(article)

        if args.output:
            generator.save_article(article, args.output)

    # ----------------------------------------

    elif args.topic:
        article = generator.create_article_from_scratch(
            topic=args.topic,
            tone=args.tone,
            length=args.length,
            keywords=args.keywords,
            style=args.style
        )

        print("\n" + "=" * 50)
        print("GENERATED ARTICLE")
        print("=" * 50)
        print(article)

        print(f"\nEstimated tokens: {generator.estimate_tokens(article)}")
        print(f"Word count: {len(article.split())}")

        if args.output:
            generator.save_article(article, args.output)

    # ----------------------------------------

    else:
        print("\nInteractive mode\n")

        topic = input("Enter article topic: ").strip()
        tone = input("Tone (professional/conversational/persuasive/educational/entertaining) [professional]: ").strip()
        tone = tone if tone else "professional"

        article = generator.create_article_from_scratch(topic, tone, config.DEFAULT_ARTICLE_LENGTH)

        print("\n" + "=" * 50)
        print("GENERATED ARTICLE")
        print("=" * 50)
        print(article)

        save = input("\nSave article? (y/n): ").lower()
        if save == "y":
            generator.save_article(article)


if __name__ == "__main__":
    main()
