# Applying Machine Learning to Static Analysis for the Fedora community

Alessandro Morari, IBM Research
Christoph Görn, Red Hat Office of the CTO

IBM Research has developed an Augmented Static Analyzer based on a [Deep Learning model called C-BERT](https://arxiv.org/pdf/2006.12641.pdf)
that is able to analyze source code in C language. They are currently using it to identify vulnerabilities in source
code, in this case, without the help of a traditional static analyzer. The C-BERT model is now one of the best in this
field based on the [CodeXGlue leaderboard](https://microsoft.github.io/CodeXGLUE/), and it could also be used for a
variety of source code tasks such as Code Completion, Code Search, Clone detection, Code translation and Code
generation.

In cooperation with the AICoE, IBM Research wants to apply this to one of the projects or communities significant to
Red Hat. The goal is to improve the code quality and developer workflows of the chosen project/community.

As C-Bert is well established for the C programming language, we are looking at the CentOS or Fedora communities first.
All their source code is available via [https://vault.centos.org/](https://vault.centos.org/) and [https://src.fedoraproject.org/](https://src.fedoraproject.org/).
As Fedora can be understood as the upstream community project of Red Hat Enterprise Linux and CoreOS, and the source
code seems to be better accessible to automation, we will focus on the Fedora community.

## Objective

Enhance the developer workflow by providing a machine-learning backed application on GitHub. The application will
automatically guide developers to focus on the most relevant static analysis issues, avoiding spending time on false
positives.

## Key Results

Analysis of the set of source code repositories, identify which repositories could benefit the most from the c-bert
application by ...

Deploy a model release pipeline on Operate First by ...

Create a prototype web service to categorize … using c-bird, deploy a CD pipeline for this app on Operate First by …

Create a GitHub app and Cronjob to use the web service to … by …

## Project Planning

TBD

## Timeline

TBD
