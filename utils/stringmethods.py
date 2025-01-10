from difflib import SequenceMatcher
import os

#closest match to a string from list
def closest(given_name, list):
    match = ""
    max_ratio = 0

    for name in list:
        distance = SequenceMatcher(None, name, given_name).ratio()
        if distance > max_ratio:
            max_ratio = distance
            match = name

    return match


#extracts word by given position in the text
def extract_word(text, pos):
    ldiff = pos
    rdiff = pos
    ln = len(text)
    lf = False
    rf = False
    while not lf or not rf:
        if ldiff >= 0 and text[ldiff] != ' ':
            ldiff -= 1
        else:
            lf = True
        if rdiff < ln and text[rdiff] != ' ':
            rdiff += 1
        else:
            rf = True

    return text[ldiff + 1 : rdiff]






def getPoem(version, id, sysnum, apps):
    applist = ""
    capplist = ""
    if len(apps) > 1:
        applist = f"{', '.join(apps[:-1])} and {apps[-1]}"
    else:
        applist = "just " + apps[0]
    
    if len(apps) - sysnum > 1:
        capplist = f"{', '.join(apps[:-1 - sysnum])} and {apps[-1 - sysnum]}"
    else:
        capplist = apps[0]
    
    id_description = ""
    if id == 0:
        id_description = "it signifies that administrative access might indeed be within reach, should the user so desire."
    else:
        id_description = "though. Consequently, the initiation of the CLIsma desktop environment under equivalent permissions could end in failure."

    ans = ""
    ans += f"""Taking into account the multitude of factors currently at play, one may discern several principal tenets concerning the present system, particularly those aspects either directly or indirectly associated with the employment of CLIsma. Possessed of certain insights and armed with the requisite authority, I deem it both prudent and, perhaps, my solemn obligation to furnish the user who has sought enlightenment on the matter of these factors and statistics with such information as I can provide.
It appears sensible to commence this endeavor with a matter of aesthetic and functional importance—namely, the version of the program in use. Hence, I shall do so without any hestiation. The present instance of CLIsma currently in execution bears the version number {version}. Given the nature of computational environments, where multiple iterations of a single program may coexist within disparate directories, it is not inconceivable that a more recent incarnation of CLIsma resides elsewhere, having already braved and surmounted the challenges of continued development.
Regarding the identity of the user initiating the program, I must confess that this information eludes my grasp. The user with id 0 might well be an ordinary individual invoking sudo, thereby assuming the identification number associated with root. Alternatively, the user could have opted to execute the program under the guise of another account, perhaps even without specific purpose or intent. Conversely, should the identifier resolved through certain methods of the os module be other than 0, emerges as token that suggests the user does not inherently possess administrative privileges. In out particular scenario that number is """
    ans += f"""{id}, {id_description}
Over the cumulative period of engagement, """
    ans += f"""the user have a total of {len(apps)} applications, listed as follows: {applist}. this figure, for all its apparent precision, excludes system applications that reside within protected directories, resistant to removal, which is and {sysnum} of them. Number of custom apps that user has installed into system is {len(apps) - sysnum} and theese apps are {capplist}. This realization provokes a curious blend of emotions, for while such system-level programs are shielded by design, it remains within the realm of possibility for the user to bypass these safeguards, should they acquire the requisite knowledge—perhaps by consulting the CLIsma wiki. It is whispered that such a repository of wisdom might reside on a certain GitHub page, though the specifics remain shrouded in uncertainty. Who is to say what truths may lie therein?"""
    return ans
