from IPython.core import interactiveshell
class TracePrinter:

    @staticmethod
    def print(trace):

        print("\n" + "=" * 60)
        print("RUNTIME TRACE")
        print("=" * 60)

        print(f"Execution ID      : {trace.execution_id}")
        print(f"Capability        : {trace.capability}")
        print(f"Objective         : {trace.objective}")

        print()

        print(
            f"Knowledge Selector: "
            f"{trace.knowledge_selector}"
        )

        print(
            f"Knowledge Docs    : "
            f"{trace.knowledge_documents}"
        )

        print(
            f"Prompt Size       : "
            f"{trace.prompt_size:,}"
        )

        print(
            f"LLM               : "
            f"{trace.llm}"
        )

        print(
            f"Elapsed           : "
            f"{trace.elapsed_ms:.0f} ms"
        )

        if trace.timeline:

            print()

            print("Timeline")

            print("-" * 40)

            for index, event in enumerate(
                trace.timeline,
                start=1,
            ):
                print(
                    f"[{index:02}] {event.name}"
                )

                print(
                    f"      elapsed: "
                    f"{event.elapsed_ms:.1f} ms"
                )

                for key, value in event.attributes.items():

                    print(
                        f"      {key}: {value}"
                    )
                    print()

        print("=" * 60)