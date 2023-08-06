use pyo3::prelude::*;
mod colorspace_transforms;
mod dct;
mod downsampling;
mod quantization;
mod arithmetic_encoding;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn JPEGAndEntropyEncoding(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(list_test,m)?)?;
    Ok(())
}

#[pyfunction]
fn list_test(mut image : Vec<Vec<Vec<usize>>>) -> Py<PyAny>{
    for i in 0..image.len(){
        for j in 0..image[0].len(){
            (image[i][j][0],image[i][j][1],image[i][j][2]) = colorspace_transforms::rgb_to_ycbcr(image[i][j][0],image[i][j][1],image[i][j][2]);
        }
    }
    return Python::with_gil(|py| image.to_object(py));
}




#[cfg(test)]

mod test{
    use pyo3::impl_::pyfunction;

    
    #[test]
    fn test1(){
        assert!(1==1);
    }
}