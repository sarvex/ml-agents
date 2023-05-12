import sys
import os

SUMMARY_XML_FILENAME = "Summary.xml"


def check_coverage(root_dir, min_percentage):
    summary_xml = next(
        (
            os.path.join(dirpath, SUMMARY_XML_FILENAME)
            for dirpath, _, filenames in os.walk(root_dir)
            if SUMMARY_XML_FILENAME in filenames
        ),
        None,
    )
    if not summary_xml:
        print(f"Couldn't find {SUMMARY_XML_FILENAME} in root directory")
        sys.exit(1)

    with open(summary_xml) as f:
        # Rather than try to parse the XML, just look for a line of the form
        # <Linecoverage>73.9</Linecoverage>
        lines = f.readlines()
        for line in lines:
            if "Linecoverage" in line:
                pct = line.replace("<Linecoverage>", "").replace("</Linecoverage>", "")
                pct = float(pct)
                if pct < min_percentage:
                    print(
                        f"Coverage {pct} is below the min percentage of {min_percentage}."
                    )
                    sys.exit(1)
                else:
                    print(
                        f"Coverage {pct} is above the min percentage of {min_percentage}."
                    )
                    sys.exit(0)

    # Couldn't find the results in the file.
    print("Couldn't find Linecoverage in summary file")
    sys.exit(1)


def main():
    min_percent = float(sys.argv[2])
    if min_percent > 0:
        root_dir = sys.argv[1]
        # This allows us to set 0% coverage on 2018.4
        check_coverage(root_dir, min_percent)


if __name__ == "__main__":
    main()
