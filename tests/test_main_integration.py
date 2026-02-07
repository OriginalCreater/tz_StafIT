import sys
import os
import tempfile
import csv


def test_script_execution(capsys):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(['country', 'year', 'gdp', 'inflation'])
        writer.writerow(['USA', '2023', '100', '3.4'])
        writer.writerow(['Russia', '2023', '50', '7.4'])
        temp_file = f.name
    try:
        original_argv = sys.argv
        sys.argv = [
            'main.py',
            '--files', temp_file,
            '--report', 'average-inflation'
        ]
        import src.main
        src.main.main()
        captured = capsys.readouterr()
        output = captured.out
        assert output != ""
        assert 'inflation' in output
    finally:
        os.unlink(temp_file)
        sys.argv = original_argv