
def PARSE(cnvrs, summary_level, prompt_type):
    """
    _summary_

    Parameters
    ----------
    cnvrs : list[dict[]]
        The conversation input. Just make a conversation with the 'discussion.py' file and use the get_messages func
    summary_level : int
        0-10, 0 = not summarised at all, 10=basically 3 words long
    prompt_type : int
        see `doc/character start int.md`, this value is that.

    Returns
    -------
    str
        The conversation, but parsed
    """
    return str(cnvrs)
