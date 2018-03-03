FROM python:3-onbuild
CMD ["python", "-m scripts.run_full_test_suite"]
