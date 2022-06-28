Landing Page (L)
    Should contain project description "Varangian is an augmented static analyzer that uses machine learning to prioritize defects identified by static analyzers based on their likelihood of being actual defects." (L1)
    List of projects whose analysis is currently available (L2)
    Link to github page (L3)
    Information regarding team and related research (L4)
        Varangian MSR paper (L4T1)
        D2A paper (L4T2)
        C-BERT paper (L4T3)
        DISCO paper (L4T4)
        Other?
Clicking on a project in the projects list (L2) will lead to the results page (R)
    This page will display actual analysis from the csv file
    The csv file will be stored in the gh-pages branch in a directory "data/<project_name>/<commit_id>"
    Only the latest commit csv file should be displayed in the defects list
    This should contain some project details (R1)
    A filter/sort for the defects list based on the following (R2)
        Error type (R2F1)
        Bug likelihood (R2F2)
        location file name (R2F3)
        Based on resolution buttons (R2F4)
    List of defects in which each defect contains the following (R3)
        Bug Location (R3D1)
        Error Type (R3D2)
        Surrounding code with context (R3D3)
        Bug trace (R3D4)
        Resolution buttons (R3D5)
            Bug - Needs Fix (R3D5R1)
                If this is selected, option to create an issue appears. Clicking on it should open a tab with the new issue template on the repo
        Bug - Does not need fix (R3D5R2)
        Not a bug (R3D5R3)
    Option to hide the defect (R3D6)

We can keep editing this list here on slack.