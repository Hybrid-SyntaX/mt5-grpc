package utils

import "errors"

func SetOptional[T any](defaultVal T, src []T) (T, error) {
	if len(src) == 0 {
		return defaultVal, nil
	}

	if len(src) > 1 {
		return defaultVal, errors.New("only one `group` allowed")
	}

	return src[0], nil
}

func Ptr[T any](v T) *T {
	return &v
}
