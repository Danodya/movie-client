from typing import Any

from requests import Response

from client_app_cli.arguments.arguments import Arguments


class PrettyPrinter:
    @staticmethod
    def pretty_print(data: dict[Any, Any], args: Arguments):
        if not data:
            print("No data to display.")
            return

        print("\n========================================\n")
        print("Results for fetched movies:\n")
        pretty_response = "\n".join(
            [
                (
                    f"Failed to fetch movies for year {key}."
                    if data[key] is None
                    else (
                        f"Year {key} has {data[key][0]} movies."
                        if args.count_only or not args.search_term
                        else f"Year {key} has {data[key][0]} movies: {data[key][1]}"
                    )
                )
                for key in data
            ]
        )
        print(pretty_response)
