from src.runtime.capabilities.rule_based import RuleBasedCapabilityDetector


def main():

    detector = RuleBasedCapabilityDetector()

    capability = detector.detect(
        "Create Pydantic models"
    )

    print(capability)


if __name__ == "__main__":
    main()