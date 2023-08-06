from pathlib import Path
from typing import Union

from gwas_sumstats_tools.interfaces.data_table import SumStatsTable
from gwas_sumstats_tools.interfaces.metadata import MetadataClient


class Formatter:
    def __init__(self) -> None:
        pass

    
def format(filename: Path,
           data_outfile: Path = None,
           minimal_to_standard: bool = False,
           generate_metadata: bool = False,
           metadata_outfile: Path = None,
           metadata_infile: Path = None,
           metadata_edit_mode: bool = False,
           metadata_from_gwas_cat: bool = False,
           custom_header_map: bool = False
           ): -> None
    
   # Set data outfile name
    ss_out = set_data_outfile_name(data_infile=filename,
                                   data_outfile=data_outfile)
    # Set metadata outfile name
    m_out = set_metadata_outfile_name(data_outfile=str(filename),
                                      metadata_outfile=metadata_outfile)
    if minimal_to_standard:
        m_out = set_metadata_outfile_name(data_outfile=ss_out,
                                          metadata_outfile=metadata_outfile)
        sst = SumStatsTable(filename)
        exit_if_no_data(table=sst.sumstats)
        print("[bold]\n-------- SUMSTATS DATA --------\n[/bold]")
        print(sst.sumstats)
        if custom_header_map:
            header_map = header_dict_from_args(args=extra_args.args)
            sst.reformat_header(header_map=header_map)
        else:
            sst.reformat_header()
        sst.normalise_missing_values()
        print("[bold]\n-------- REFORMATTED DATA --------\n[/bold]")
        print(sst.sumstats)
        print(f"[green]Formatting and writing sumstats data --> {ss_out}[/green]")
        with Progress(SpinnerColumn(finished_text="Complete!"),
                      TextColumn("[progress.description]{task.description}"),
                      transient=True
                      ) as progress:
            progress.add_task(description="Processing...", total=None)
            sst.to_file(outfile=ss_out)
    # Get metadata
    if generate_metadata:
        print("[bold]\n---------- METADATA ----------\n[/bold]")
        meta_dict = get_file_metadata(in_file=filename, out_file=ss_out)
        if metadata_from_gwas_cat:
            meta_dict = metadata_dict_from_gwas_cat(accession_id=parse_accession_id(filename=filename))
        if metadata_edit_mode:
            meta_dict.update(metadata_dict_from_args(args=extra_args.args))
        ssm = MetadataClient(out_file=m_out,
                             in_file=metadata_infile)
        ssm.update_metadata(data_dict=meta_dict)
        print(ssm)
        print(f"[green]Writing metadata --> {m_out}[/green]")
        ssm.to_file()
    if not any([minimal_to_standard, generate_metadata]):
        print("Nothing to do.")