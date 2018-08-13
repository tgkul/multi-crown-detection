from sklearn.metrics import mean_squared_error


def get_mse(arr1, arr2):
    mse = mean_squared_error(arr1, arr2)
    return mse
