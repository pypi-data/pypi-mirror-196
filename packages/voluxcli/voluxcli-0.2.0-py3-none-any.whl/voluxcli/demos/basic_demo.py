from volux import VoluxDemo


class BasicDemo(VoluxDemo):
    id = "basic"
    description = "A simple demo with a simple source, transformer and destination."
    DEV__requirements = [
        {"distribution_name": "voluxexamplemodule", "version_requirement": ">=0.10.0"},
    ]

    @staticmethod
    def main():
        from voluxexamplemodule import VoluxNumber, VoluxMultiply, VoluxCliBar

        with VoluxNumber(_min=0, _max=10) as vlxn:
            with VoluxMultiply(10) as vlx_mult:
                with VoluxCliBar() as vlx_clibar:
                    for _ in range(5):
                        vlx_clibar.print(
                            vlx_mult.multiply(vlxn.generate_number),
                            max_segments=100,
                        )


if __name__ == "__main__":
    BasicDemo().main()
