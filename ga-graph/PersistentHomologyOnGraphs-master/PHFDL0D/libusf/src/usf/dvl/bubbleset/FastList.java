package usf.dvl.bubbleset;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.Set;

/**
 * An subclass of the {@link ArrayList} with a very fast
 * {@link #contains(Object)} method. {@link ArrayList#indexOf(Object)
 * indexOf(Object)} and {@link ArrayList#lastIndexOf(Object)
 * lastIndexOf(Object)} are not faster though. Unfortunately this results in
 * following methods that cannot be used anymore:
 * <ul>
 * <li> {@link #remove(int)}
 * <li>{@link #remove(Object)}
 * <li>{@link #removeAll(Collection)}
 * <li>{@link #removeRange(int, int)}
 * <li>{@link #retainAll(Collection)}
 * <li>{@link #set(int, Object)}
 * <li>{@link #clone()}
 * </ul>
 * 
 * @author Joschi <josua.krause@googlemail.com>
 * @param <E> The type parameter.
 */
public final class FastList<E> extends ArrayList<E> {

  /** The serial version uid. */
  private static final long serialVersionUID = 2901108923922468511L;

  /** The hash set for the fast existence lookup. */
  private final Set<E> set = new HashSet<E>();

  /**
   * Creates a fast list. {@linkPlain ArrayList#ArrayList()}
   */
  public FastList() {
    super();
  }

  /**
   * Creates a fast list. {@linkPlain ArrayList#ArrayList(int)}
   * 
   * @param size The ensured capacity of the list.
   */
  public FastList(final int size) {
    super(size);
  }

  /**
   * Creates a fast list. {@linkPlain ArrayList#ArrayList(Collection)}
   * 
   * @param c The initial content.
   */
  public FastList(final Collection<? extends E> c) {
    super(c);
    set.addAll(c);
  }

  @Override
  public boolean add(final E e) {
    set.add(e);
    return super.add(e);
  }

  @Override
  public void add(final int index, final E element) {
    set.add(element);
    super.add(index, element);
  }

  @Override
  public boolean addAll(final Collection<? extends E> c) {
    set.addAll(c);
    return super.addAll(c);
  }

  @Override
  public boolean addAll(final int index, final Collection<? extends E> c) {
    set.addAll(c);
    return super.addAll(index, c);
  }

  @Override
  public boolean contains(final Object o) {
    return set.contains(o);
  }

  @Override
  public boolean containsAll(final Collection<?> c) {
    return set.containsAll(c);
  }

  @Override
  public void clear() {
    set.clear();
    super.clear();
  }

  @Override
  public E remove(final int index) {
    throw new UnsupportedOperationException();
  }

  @Override
  public boolean remove(final Object o) {
    throw new UnsupportedOperationException();
  }

  @Override
  public boolean removeAll(final Collection<?> c) {
    throw new UnsupportedOperationException();
  }

  @Override
  protected void removeRange(final int fromIndex, final int toIndex) {
    throw new UnsupportedOperationException();
  }

  @Override
  public boolean retainAll(final Collection<?> c) {
    throw new UnsupportedOperationException();
  }

  @Override
  public E set(final int index, final E element) {
    throw new UnsupportedOperationException();
  }

}
